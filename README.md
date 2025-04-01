# Google Scraper with Selenium and PostgreSQL

A simple web scraper that retrieves Google search results based on user input and stores the data in a CSV file as well as a PostgreSQL database.

## Features
- **Interactive Input**: Enter a search term (or `exit` to quit).
- **Data Extraction**: Titles, links, and descriptions from Google search results.
- **Storage**: 
  - CSV file (`results.csv`).
  - PostgreSQL database (Schema: `google_scraper`, Table: `search_results`).
- **Error Handling**: Messages for connection issues or missing results.

## Prerequisites
- **Python 3.8+**: [Download](https://www.python.org/downloads/)
- **Google Chrome**: With matching [ChromeDriver](https://chromedriver.chromium.org/downloads)
- **Docker**: For PostgreSQL [Install](https://www.docker.com/get-started)
- **Python Packages**: `selenium`, `beautifulsoup4`, `pandas`, `sqlalchemy`, `pg8000`

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Felip123/ScrapingMitPython.git
cd ScrapingMitPython