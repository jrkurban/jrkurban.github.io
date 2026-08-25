"""
RSS kaynaklarini ceker, tekrar eden haberleri eler, data/news.json'a yazar.
Bu dosya build_site.py tarafindan okunup statik HTML'e donusturulur.
"""

import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path

import feedparser

from feeds import FEEDS

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "news.json"
MAX_AGE_DAYS = 14  # bu sureden eski haberler listeden dusurulur
MAX_ITEMS = 120  # dosyada tutulan maksimum haber sayisi


def make_id(entry, source_name: str) -> str:
    """Bir haberi tekilleyen kararli bir kimlik uretir (link varsa onu kullanir)."""
    raw = entry.get("id") or entry.get("link") or (source_name + entry.get("title", ""))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def parse_published(entry) -> str:
    """Yayin tarihini ISO 8601 string'e cevirir, bulamazsa simdiki zamani kullanir."""
    for key in ("published_parsed", "updated_parsed"):
        value = entry.get(key)
        if value:
            return datetime(*value[:6], tzinfo=timezone.utc).isoformat()
    return datetime.now(timezone.utc).isoformat()


def clean_summary(entry) -> str:
    text = entry.get("summary", "") or ""
    # Cok basit bir HTML temizligi - ozet alaninda genelde ufak taglar olur
    import re

    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:280]


def load_existing() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return {item["id"]: item for item in json.load(f)}
    return {}


def fetch_all() -> list:
    existing = load_existing()
    fetched_at = datetime.now(timezone.utc).isoformat()

    for source in FEEDS:
        try:
            parsed = feedparser.parse(source["url"])
        except Exception as exc:  # kaynak coktu diye tum site cokmemeli
            print(f"[uyari] {source['name']} okunamadi: {exc}")
            continue

        for entry in parsed.entries:
            item_id = make_id(entry, source["name"])
            if item_id in existing:
                continue  # zaten kayitli, tekrar ekleme
            existing[item_id] = {
                "id": item_id,
                "title": (entry.get("title") or "(baslik yok)").strip(),
                "link": entry.get("link", ""),
                "summary": clean_summary(entry),
                "published": parse_published(entry),
                "source": source["name"],
                "kind": source["kind"],
                "first_seen": fetched_at,
            }

    # eskileri temizle ve siraya diz
    cutoff = time.time() - MAX_AGE_DAYS * 86400
    items = [
        v
        for v in existing.values()
        if datetime.fromisoformat(v["published"]).timestamp() > cutoff
    ]
    items.sort(key=lambda x: x["published"], reverse=True)
    return items[:MAX_ITEMS]


def main():
    items = fetch_all()
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"{len(items)} haber data/news.json dosyasina yazildi.")


if __name__ == "__main__":
    main()
