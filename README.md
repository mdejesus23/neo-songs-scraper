# 🎼 Liturgical Song Image Scraper

This Python script scrapes liturgical song pages from the [Neocatechumenal Way Liturgical Songs](https://neocatechumenalway.wixsite.com/song/liturgical) website and downloads associated song images that are exactly 800 pixels wide. The images are stored locally in the `images/liturgical/` directory.

---

## 📌 Features

- 🔍 Automatically collects links to individual liturgical songs
- 🌐 Visits each song subpage
- 🖼 Extracts and downloads images that are 800px wide
- 🧼 Sanitizes filenames to avoid issues
- 📁 Automatically creates required folders
- 💤 Adds a polite delay between requests to avoid overwhelming the server

---

## 🧰 Requirements

You need Python 3 and the following Python packages:

- `requests`
- `beautifulsoup4`

Install the required libraries using pip:

```bash
pip install requests beautifulsoup4
