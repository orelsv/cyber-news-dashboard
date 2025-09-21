import os
import json
import time
from datetime import datetime
from typing import List, Dict

import requests
from flask import (
    Flask, render_template, request, jsonify,
    send_from_directory, redirect, url_for
)

# --- Load .env so NEWSAPI_KEY is available locally ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- Paths / config ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
ADMIN_DIR  = os.path.join(STATIC_DIR, "admin")   # built React admin goes here
CONFIG_DIR = os.path.join(BASE_DIR, "config")
SETTINGS_PATH = os.path.join(CONFIG_DIR, "settings.json")

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
APP_BUILD_VERSION = os.getenv("BUILD_VERSION") or str(int(time.time()))

app = Flask(__name__, static_folder="static", template_folder="templates")

# --- Make helpers available in all templates ---
@app.context_processor
def inject_globals():
    return {
        "now": datetime.now,           # usage: {{ now().year }}
        "build_version": APP_BUILD_VERSION,  # cache-busting for CSS/JS
    }

# --- Jinja filter: ISO -> "YYYY-MM-DD HH:MM" ---
@app.template_filter("format_iso")
def format_iso(value: str) -> str:
    try:
        if not value:
            return ""
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return value or ""

# --- Settings I/O (used by admin UI) ---
def load_settings() -> Dict:
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "keywords": "cybersecurity, malware, phishing",
            "article_count": 12,
            "refresh_minutes": 30,
        }

def save_settings(data: dict):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- News fetching with pagination + dedup until we meet requested count ---
def _normalize_articles(raw: List[Dict]) -> List[Dict]:
    """Map NewsAPI articles to template-friendly dicts."""
    out = []
    for art in raw or []:
        out.append({
            "title": art.get("title"),
            "description": art.get("description"),
            "url": art.get("url"),
            "image": art.get("urlToImage"),
            "source": (art.get("source") or {}).get("name"),
            "published": art.get("publishedAt"),
        })
    return out

def _fetch_newsapi(term: str, page_size: int, page: int = 1) -> List[Dict]:
    """
    Single call to NewsAPI /v2/everything for a term and page.
    Returns raw list of articles; logs errors for debugging.
    """
    if not NEWSAPI_KEY:
        print("[NEWSAPI] Missing NEWSAPI_KEY")
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": term,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": min(max(page_size, 1), 100),  # NewsAPI max 100
        "page": max(page, 1),
    }
    headers = {"X-Api-Key": NEWSAPI_KEY}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=12)
        if r.status_code != 200:
            print(f"[NEWSAPI] HTTP {r.status_code} for q='{term}', page={page}: {r.text[:300]}")
            return []
        data = r.json()
        return data.get("articles", []) or []
    except Exception as e:
        print(f"[NEWSAPI] Request error for q='{term}', page={page}: {e}")
        return []

def fetch_articles(keywords: str, total_needed: int = 10) -> List[Dict]:
    """
    Build up to `total_needed` unique articles by:
    - splitting keywords by comma/semicolon into terms,
    - paginating per term,
    - deduplicating by URL,
    - continuing until we hit requested count or exhaust results.
    """
    terms = [t.strip() for t in keywords.replace(";", ",").split(",") if t.strip()]
    if not terms:
        terms = ["cybersecurity"]

    results: List[Dict] = []
    seen_urls = set()

    # Limits to avoid hammering the API (tune if needed)
    MAX_PAGES_PER_TERM = 3
    for term in terms:
        if len(results) >= total_needed:
            break

        page = 1
        while page <= MAX_PAGES_PER_TERM and len(results) < total_needed:
            need_now = min(100, max(1, total_needed - len(results)))
            raw = _fetch_newsapi(term, page_size=need_now, page=page)
            if not raw:
                break

            for a in _normalize_articles(raw):
                url = a.get("url")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                results.append(a)
                if len(results) >= total_needed:
                    break

            page += 1

    if len(results) < total_needed:
        print(f"[NEWSAPI] Collected {len(results)}/{total_needed} articles "
              f"(API returned fewer items or duplicates were filtered).")

    return results[:total_needed]

# --- Routes: site ---
@app.route("/", endpoint="index")
def home():
    settings = load_settings()
    keywords = settings.get("keywords", "cybersecurity")
    article_count = int(settings.get("article_count", 10))
    articles = fetch_articles(keywords, article_count)
    return render_template(
        "index.html",
        articles=articles,
        default_query=keywords,
        settings=settings,
    )

@app.route("/search")
def search():
    settings = load_settings()
    raw_q = (request.args.get("q") or "").strip()
    effective_q = raw_q or settings.get("keywords", "cybersecurity")
    article_count = int(settings.get("article_count", 10))
    articles = fetch_articles(effective_q, article_count)
    try:
        return render_template(
            "search.html",
            q=raw_q,
            effective_q=effective_q,
            articles=articles,
            settings=settings,
        )
    except Exception:
        return redirect(url_for("index"))

# --- API: admin settings ---
@app.route("/api/settings", methods=["GET", "POST"])
def api_settings():
    if request.method == "GET":
        return jsonify(load_settings())

    data = request.get_json(force=True) or {}
    settings = {
        "keywords": str(data.get("keywords", "cybersecurity")).strip(),
        "article_count": max(1, int(data.get("article_count", 10))),
        "refresh_minutes": max(1, int(data.get("refresh_minutes", 30))),
    }
    save_settings(settings)
    return jsonify({"ok": True, "settings": settings})

# --- Serve built React Admin (/admin and its assets) ---
@app.route("/admin/")
def admin_index():
    return send_from_directory(ADMIN_DIR, "index.html")

@app.route("/admin/<path:filename>")
def admin_static(filename):
    return send_from_directory(ADMIN_DIR, filename)

# Optional fallback for builds that reference absolute /assets/...
@app.route("/assets/<path:filename>")
def admin_assets_root(filename):
    return send_from_directory(os.path.join(ADMIN_DIR, "assets"), filename)

# --- Run app ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", "81"))
    app.run(host="0.0.0.0", port=port)