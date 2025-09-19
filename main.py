# main.py
import os
import requests
from time import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

# ---------- Paths (explicit & stable) ----------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# ---------- Load environment ----------
# Load .env BEFORE reading env vars (works locally; on Replit use Secrets)
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

# ---------- App ----------
# Explicit folders avoid “where are my templates/static?” issues on some hosts.
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# Optional cache-busting for static assets (safe in prod; deterministic if file mtime available)
def _static_build_version() -> int:
    """
    Returns a revision number for static assets to avoid stale browser caches.
    Uses styles.css mtime if available; falls back to current epoch.
    """
    candidate = os.path.join(STATIC_DIR, "css", "styles.css")
    try:
        return int(os.path.getmtime(candidate))
    except Exception:
        return int(time())

@app.context_processor
def inject_build_version():
    # Expose `build_version` for `...?v={{ build_version }}` in templates
    return {"build_version": _static_build_version()}

# ---------- External API config ----------
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
if not NEWSAPI_KEY:
    raise RuntimeError("NEWSAPI_KEY is not set. Add it to your environment or .env.")

DEFAULT_QUERY = 'cybersecurity OR malware OR "information security"'
PAGE_SIZE = 20

# ---------- Helpers ----------
def fetch_articles(query: str, page_size: int = PAGE_SIZE):
    """
    Query NewsAPI 'everything' endpoint and normalize fields for templates.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    items = resp.json().get("articles", [])

    normalized = []
    for a in items:
        normalized.append({
            "title": (a.get("title") or "Untitled").strip(),
            "description": (a.get("description") or "").strip(),
            "url": a.get("url"),
            "image": a.get("urlToImage") or "",  # keep empty string to avoid broken images
            "source": (a.get("source") or {}).get("name") or "Unknown",
            "published": a.get("publishedAt") or "",
        })
    return normalized

def format_iso(ts: str) -> str:
    """
    Format ISO timestamp (e.g. '2025-09-19T08:33:12Z') into 'YYYY-MM-DD HH:MM'.
    """
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts

# Register Jinja filter once
app.jinja_env.filters['format_iso'] = format_iso

# ---------- Routes ----------
@app.route("/")
def index():
    """
    Home feed using a default cybersecurity-centric query.
    """
    articles = fetch_articles(DEFAULT_QUERY)
    return render_template("index.html", articles=articles, default_query=DEFAULT_QUERY)

@app.route("/search")
def search():
    """
    Search endpoint: GET /search?q=term
    Redirects home when query is empty.
    """
    q = (request.args.get("q") or "").strip()
    if not q:
        return redirect(url_for("index"))
    articles = fetch_articles(q)
    return render_template("search.html", articles=articles, q=q)

# ---------- Entrypoint ----------
if __name__ == "__main__":
    # Replit-friendly default; locally you can `export PORT=5000` if you prefer.
    port = int(os.getenv("PORT", "81"))
    app.run(host="0.0.0.0", port=port, debug=False)