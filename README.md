# Google-Scraper mit Selenium und PostgreSQL

Ein einfacher Web-Scraper, der Google-Suchergebnisse abruft und in CSV und PostgreSQL speichert.

## Funktionen
- **Eingabe**: Suchbegriff interaktiv.
- **Datenextraktion**: Titel, Links, Beschreibungen von Google.
- **Speicherung**: CSV (`results.csv`), PostgreSQL (Schema: `google_scraper`, Tabelle: `search_results`).

## Voraussetzungen
- Python 3.8+
- Google Chrome (mit [ChromeDriver](https://chromedriver.chromium.org/downloads))
- Docker (für PostgreSQL)
- Pakete: `selenium`, `beautifulsoup4`, `pandas`, `sqlalchemy`, `pg8000`

## Einrichtung
1. **Repository klonen**:
   ```bash
   git clone https://github.com/Felip123/ScrapingMitPython.git
   cd ScrapingMitPython