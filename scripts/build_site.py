"""
data/news.json dosyasini okuyup docs/index.html olarak statik bir sayfa uretir.
docs/ klasoru GitHub Pages tarafindan servis edilecek klasordur.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "news.json"
DOCS_DIR = ROOT / "docs"

GERMAN_DAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
GERMAN_MONTHS = [
    "", "Januar", "Februar", "Marz", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
]


def format_date_de(dt: datetime) -> str:
    return f"{GERMAN_DAYS[dt.weekday()]}, {dt.day}. {GERMAN_MONTHS[dt.month]} {dt.year}"


def format_time_de(dt: datetime) -> str:
    return dt.strftime("%H:%M")


def load_items() -> list:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def group_by_day(items: list) -> dict:
    groups = defaultdict(list)
    for item in items:
        dt = datetime.fromisoformat(item["published"])
        key = dt.date().isoformat()
        groups[key].append((dt, item))
    return dict(sorted(groups.items(), reverse=True))


CARD_TEMPLATE = """
<article class="card">
  <div class="card-meta">
    <span class="card-time">{time}</span>
    <span class="card-source">{source}</span>
  </div>
  <h3 class="card-title"><a href="{link}" target="_blank" rel="noopener">{title}</a></h3>
  <p class="card-summary">{summary}</p>
</article>
"""

DAY_TEMPLATE = """
<section class="day-group">
  <div class="day-divider">
    <span class="day-label">{day_label}</span>
    <svg class="headframe" viewBox="0 0 60 40" aria-hidden="true">
      <path d="M10 38 L30 4 L50 38 M18 38 L30 16 L42 38 M6 38 H54" />
      <circle cx="30" cy="9" r="2.4" />
    </svg>
  </div>
  <div class="card-grid">
    {cards}
  </div>
</section>
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bochum Aktuell &mdash; Lokale Nachrichten gebuendelt</title>
<meta name="description" content="Automatisch gebuendelte lokale Nachrichten aus Bochum.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="shift-board">
  <div class="shift-board-inner">
    <span class="shift-label">BOCHUM AKTUELL</span>
    <span class="shift-status">STAND&nbsp;&mdash;&nbsp;{updated}</span>
  </div>
</header>

<main>
  <div class="intro">
    <h1>Was in Bochum passiert.</h1>
    <p>Automatisch gebuendelt aus staedtischen Meldungen, Behoerden und lokaler Presse. Aktualisiert bei jedem Durchlauf &mdash; keine Anmeldung, kein Rauschen.</p>
  </div>

  {day_sections}

  {empty_state}
</main>

<footer>
  <p>Quellen: Stadt Bochum, Landgericht Bochum, lokale Presse via Google&nbsp;News. Erzeugt mit Python + GitHub&nbsp;Actions. Kein redaktioneller Eingriff &mdash; reine Buendelung oeffentlicher Feeds.</p>
</footer>
</body>
</html>
"""

EMPTY_STATE = """
<div class="empty-state">
  <p>Noch keine Daten. Der erste automatische Lauf fuellt diese Seite.</p>
</div>
"""


def build():
    items = load_items()
    groups = group_by_day(items)

    day_sections_html = []
    for day_key, entries in groups.items():
        day_dt = entries[0][0]
        cards_html = "".join(
            CARD_TEMPLATE.format(
                time=format_time_de(dt),
                source=item["source"],
                link=item["link"],
                title=item["title"],
                summary=item["summary"],
            )
            for dt, item in entries
        )
        day_sections_html.append(
            DAY_TEMPLATE.format(day_label=format_date_de(day_dt), cards=cards_html)
        )

    now = datetime.now(timezone.utc)
    page = PAGE_TEMPLATE.format(
        updated=now.strftime("%d.%m.%Y %H:%M UTC"),
        day_sections="".join(day_sections_html),
        empty_state=EMPTY_STATE if not items else "",
    )

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    with open(DOCS_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(page)
    print(f"docs/index.html uretildi ({len(items)} haber, {len(groups)} gun).")


if __name__ == "__main__":
    build()
