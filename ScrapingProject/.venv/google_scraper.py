from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import Error
import urllib.parse

# Database connection parameters (for Dockerized Postgres)
DB_PARAMS = {
    "dbname": "google_scraper",
    "user": "postgres",
    "password": "mysecretpassword",
    "host": "localhost",
    "port": "5432"
}

# ChromeDriver setup
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(), options=options)  # Adjust path if needed


def connect_to_db():
    try:
        connection = psycopg2.connect(**DB_PARAMS)
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def save_to_db(connection, query, results):
    try:
        cursor = connection.cursor()
        for result in results:
            cursor.execute("""
                INSERT INTO google_scraper.search_results (search_query, title, link, description)
                VALUES (%s, %s, %s, %s)
            """, (query, result.get('title'), result.get('link'), result.get('description')))
        connection.commit()
        print("Data successfully saved to database")
    except Error as e:
        print(f"Error saving to database: {e}")
        connection.rollback()
    finally:
        cursor.close()


# Get URL from user input and extract query
custom_url = input("Please enter the URL you want to scrape: ")
parsed_url = urllib.parse.urlparse(custom_url)
query = urllib.parse.parse_qs(parsed_url.query).get('q', [''])[0]  # Extract 'q' parameter (e.g., "hello")
driver.get(custom_url)

# Wait for page to load
time.sleep(2)

page_html = driver.page_source
soup = BeautifulSoup(page_html, 'html.parser')
results = []

# Scrape logic
try:
    allData = soup.find("div", {"class": "dURPMd"}).find_all("div", {"class": "Ww4FFb"})
    print(f"Found {len(allData)} results")

    for item in allData:
        obj = {}
        try:
            title = item.find("h3").text[:100]  # Limit to 100 chars
            obj["title"] = title if title else None
        except:
            obj["title"] = None
        try:
            link = item.find("a").get('href')[:200]  # Limit to 200 chars
            obj["link"] = link if link else None
        except:
            obj["link"] = None
        try:
            desc = item.find("div", {"class": "VwiC3b"}).text[:300]  # Limit to 300 chars
            obj["description"] = desc if desc else None
        except:
            obj["description"] = None
        results.append(obj)

except AttributeError:
    print("Using fallback scraping for non-Google pages")
    titles = soup.find_all(['h1', 'h2', 'h3'])
    links = soup.find_all('a', href=True)

    for title in titles:
        results.append({"title": title.text.strip()[:100], "link": None, "description": None})
    for link in links:
        if link.text.strip():
            results.append({"title": link.text.strip()[:100], "link": link.get('href')[:200], "description": None})

# Save to database
connection = connect_to_db()
if connection:
    save_to_db(connection, query, results)
    connection.close()

driver.quit()