# ScrapingMitPython
Challenge from the module 122 in TBZ school

# Web Scraper with Dockerized PostgreSQL

## Beschreibung
Dieses Projekt scrapt Webseiten direkt ohne API und speichert die Ergebnisse in einer PostgreSQL-Datenbank, die in einem Docker-Container läuft. Es ist parametrisierbar mit benutzerdefinierten URLs.

## Voraussetzungen
- Docker Desktop
- Python 3.x (local)
- ChromeDriver (local)

## Installation
1. Starte PostgreSQL in Docker:
   ```powershell
   docker run -d --name postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=google_scraper -p 5432:5432 postgres:13