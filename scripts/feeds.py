"""
Bochum icin haber kaynaklari.
Her feed bir dict: name (goruntulenen ad), url (RSS/Atom adresi), kind (site|behoerde|suche)

NOT: Bazi yerel siteler zamanla RSS adreslerini degistirebilir. Bu yuzden
Google News RSS aramasi (kind="suche") her zaman calisan bir yedek/ana kaynak
olarak eklendi - herhangi bir resmi feed kirilirsa site yine de bos kalmaz.
"""

FEEDS = [
    {
        "name": "Stadt Bochum (offiziell)",
        "url": "https://www.bochum.de/RSSNews.xml",
        "kind": "behoerde",
    },
    {
        "name": "Landgericht Bochum",
        "url": "https://www.lg-bochum.nrw.de/behoerde/rss/pressemitteilungen.php",
        "kind": "behoerde",
    },
    {
        "name": "Google News: Bochum",
        "url": "https://news.google.com/rss/search?q=Bochum&hl=de&gl=DE&ceid=DE:de",
        "kind": "suche",
    },
    {
        "name": "Google News: Bochum Innenstadt",
        "url": "https://news.google.com/rss/search?q=%22Bochum%22%20Innenstadt&hl=de&gl=DE&ceid=DE:de",
        "kind": "suche",
    },
]

# Bu kelimelerden en az biri baslikta/ozet metninde geciyorsa haber "on plana" alinir.
# Bos birakilirsa hicbir on plan filtrelemesi yapilmaz, her sey normal sirada gosterilir.
HIGHLIGHT_KEYWORDS = [
    "Innenstadt",
    "Wattenscheid",
    "Ruhr-Universitat",
    "Bahn",
    "Polizei",
    "Wetter",
]
