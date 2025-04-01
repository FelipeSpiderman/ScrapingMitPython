from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine



CHROMEDRIVER_PATH = "C:/Work/Git/ScrapingMitPython/chromedriver-win64/chromedriver.exe"


service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()


options.add_argument("--window-size=1920,1080")  # Set window size
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=service, options=options)

# Open Google Search URL
search_url = "https://www.google.com/search?q=lead+generation+tools&oq=lead+generation+tools"

driver.get(search_url)

# Wait for the page to load
time.sleep(2)

page_html = driver.page_source

soup = BeautifulSoup(page_html,'html.parser')
obj={}
l=[]
allData = soup.find("div",{"class":"dURPMd"}).find_all("div",{"class":"Ww4FFb"})
print(len(allData))
for i in range(0,len(allData)):
    try:
        obj["title"]=allData[i].find("h3").text
    except:
        obj["title"]=None

    try:
        obj["link"]=allData[i].find("a").get('href')
    except:
        obj["link"]=None

    try:
        obj["description"]=allData[i].find("div",{"class":"VwiC3b"}).text
    except:
        obj["description"]=None

    l.append(obj)
    obj={}

df = pd.DataFrame(l)
df.to_csv('google.csv', index=False, encoding='utf-8')

engine = create_engine("postgresql+pg8000://postgres:postgres@localhost:5432/postgres")
df.to_sql('search_results', engine, schema="google_scraper", if_exists='append', index=False)

print(l)