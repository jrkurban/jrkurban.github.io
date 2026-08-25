# Bochum Aktuell

Bochum icin yerel haberleri otomatik toplayan, tekrarlari eleyen ve
GitHub Pages'te statik bir sayfa olarak yayinlayan kucuk bir Python projesi.

**Canli site:** `https://<kullanici-adin>.github.io/<repo-adin>/` (kurulumdan sonra)

## Nasil calisir

```
scripts/feeds.py        -> takip edilen RSS/Atom kaynaklarinin listesi
scripts/fetch_news.py   -> kaynaklari ceker, tekilleştirir, data/news.json'a yazar
scripts/build_site.py   -> data/news.json'dan docs/index.html uretir
.github/workflows/      -> GitHub Actions ile gunde 2 kez otomatik calistirir ve commitler
```

GitHub Pages, `docs/` klasorunu sunucusuz olarak servis eder. Yani hicbir
sunucuya veya API'ye ihtiyac yoktur - GitHub Actions verileri ceker,
HTML'i uretir ve repoya geri commitler; Pages de bu dosyayi yayinlar.

## Kaynaklar

- Stadt Bochum resmi RSS akisi
- Landgericht Bochum basin aciklamalari
- Google News araması (yerel Bochum haberleri icin genis kapsamli yedek kaynak)

Kaynak listesini `scripts/feeds.py` icinde degistirebilir, yeni RSS adresleri
ekleyebilir veya `HIGHLIGHT_KEYWORDS` ile kendi mahallene ozel anahtar
kelimeler tanimlayabilirsin (orn. oturdugun semt).

## Kurulum

1. Bu klasoru bir GitHub reposuna push'la.
2. Repo ayarlarinda **Settings > Pages > Source** kismindan `main` dalinda
   `/docs` klasorunu sec.
3. **Settings > Actions > General > Workflow permissions** kismindan
   "Read and write permissions" sec (workflow'un commit atabilmesi icin).
4. Actions sekmesinden `Bochum Aktuell aktualisieren` workflow'unu elle bir
   kez calistir (`workflow_dispatch`) - ilk veri boylece hemen olusur.

Bundan sonra site gunde iki kez otomatik guncellenir.

## Yerel gelistirme

```bash
pip install -r requirements.txt
python scripts/fetch_news.py   # data/news.json'u gunceller
python scripts/build_site.py   # docs/index.html'i uretir
```

`docs/index.html`'i tarayicida acarak sonucu gorebilirsin.

## Genisletme fikirleri

- Baska bir Alman sehri icin `scripts/feeds.py`'yi kopyala/uyarla.
- `HIGHLIGHT_KEYWORDS` ile ilgi alanina gore haberleri one cikar.
- RSS'i olmayan bir siteyi eklemek icin basit bir scraper yaz ve
  `fetch_news.py` icindeki akisa entegre et.
