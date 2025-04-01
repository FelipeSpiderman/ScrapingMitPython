from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# ChromeDriver setup
CHROMEDRIVER_PATH = "C:/Work/Git/ScrapingMitPython/chromedriver-win64/chromedriver.exe"
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=service, options=options)

search_query = input("Enter your search terms (or 'exit' to quit): ")
if search_query.lower() == 'exit':
    driver.quit()

# Google search URL
encoded_query = urllib.parse.quote(search_query)
search_url = f"https://www.google.com/search?q={encoded_query}"
driver.get(search_url)
time.sleep(2)

# Parse page
page_html = driver.page_source
soup = BeautifulSoup(page_html, 'html.parser')

# Extract data
obj, l = {}, []
container = soup.find("div", {"class": "dURPMd"})
if container:
    allData = container.find_all("div", {"class": "Ww4FFb"})
else:
    allData = []
    print("Keine Ergebnisse gefunden. HTML-Struktur möglicherweise geändert.")

print(f"Found {len(allData)} results")
for i in range(len(allData)):
    try:
        obj["title"] = allData[i].find("h3").text
    except:
        obj["title"] = None
    try:
        obj["link"] = allData[i].find("a").get('href')
    except:
        obj["link"] = None
    try:
        obj["description"] = allData[i].find("div", {"class": "VwiC3b"}).text
    except:
        obj["description"] = None
    l.append(obj)
    obj = {}

# Save to CSV
df = pd.DataFrame(l)
df.to_csv('results.csv', index=False, encoding='utf-8')

# Database
engine_db = create_engine("postgresql+pg8000://postgres:postgres@localhost:5432/postgres")
try:
    with engine_db.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
    driver.quit()
    exit()

try:
    with engine_db.begin() as connection:
        df.to_sql('search_results', engine_db, schema="google_scraper", if_exists='append', index=False)
    print("Data written to database successfully!")
except Exception as e:
    print(f"Failed to write to database: {e}")

print(l)

driver.quit()