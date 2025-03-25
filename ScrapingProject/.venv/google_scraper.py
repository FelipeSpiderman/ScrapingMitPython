from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def scrape_google(query, num_results=10):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    url = f"https://www.google.com/search?q={query}&num={num_results}"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
        )
    except:
        print("Timeout waiting for search results")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    results = []
    for i, result in enumerate(soup.select("div.g"), start=1):
        title = result.select_one("h3")
        link = result.select_one("a")
        description = result.select_one("span.st")

        if title and link:
            print(f"Ergebnis {i}: {title.get_text()}")
            results.append({
                "title": title.get_text(),
                "link": link["href"],
                "description": description.get_text() if description else "",
                "position": i
            })

    driver.quit()
    print(f"Anzahl gefundener Ergebnisse: {len(results)}")
    return results