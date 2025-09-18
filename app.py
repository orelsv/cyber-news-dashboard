import os
import time
import requests
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Simple in-memory cache to avoid hitting API too often during development
_cache = {"ts": 0, "data": []}
CACHE_TTL_SECONDS = 300  # 5 minutes

def fetch_news():
    """
    Fetch technology/cybersecurity related headlines from NewsAPI.
    We use 'everything' endpoint with query filters. Keep it simple and robust.
    """
    global _cache
    now = time.time()
    if (now - _cache["ts"]) < CACHE_TTL_SECONDS and _cache["data"]:
        return _cache["data"]

    if not NEWSAPI_KEY:
        # If key is missing, return placeholder items with instructions
        return [
            {
                "title": "Set NEWSAPI_KEY in your .env file",
                "description": "Create a .env file with NEWSAPI_KEY=your_key to fetch live news.",
                "url": "https://newsapi.org/",
                "source": {"name": "Setup"},
                "publishedAt": ""
            }
        ]

    url = "https://newsapi.org/v2/everything"
    params = {
        # Query for cybersecurity/infosec/technology topics
        "q": "(cybersecurity OR infosec OR malware OR hacking OR \"data breach\" OR security) OR technology",
        "language": "en",
        "pageSize": 15,
        "sortBy": "publishedAt",
    }
    headers = {"X-Api-Key": NEWSAPI_KEY}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        articles = data.get("articles", [])
        # Keep only the fields we actually use to avoid surprises
        simplified = []
        for a in articles:
            simplified.append(
                {
                    "title": a.get("title") or "No title",
                    "description": a.get("description") or "",
                    "url": a.get("url") or "#",
                    "source": {"name": (a.get("source") or {}).get("name", "Unknown")},
                    "publishedAt": a.get("publishedAt") or ""
                }
            )
        _cache = {"ts": now, "data": simplified}
        return simplified
    except requests.RequestException:
        # Graceful fallback
        return [
            {
                "title": "Unable to fetch news right now",
                "description": "Please try again later. This could be a network or API limit issue.",
                "url": "#",
                "source": {"name": "Fallback"},
                "publishedAt": ""
            }
        ]


@app.route("/")
def home():
    """
    Render the homepage with a list of articles.
    """
    articles = fetch_news()
    return render_template("index.html", articles=articles)


if __name__ == "__main__":
    # For local dev: http://127.0.0.1:5048
    app.run(host="0.0.0.0", port=5048, debug=True)