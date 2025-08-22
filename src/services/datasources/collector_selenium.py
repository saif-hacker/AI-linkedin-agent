import os
import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")
SEARCH_QUERY = os.getenv("LINKEDIN_SEARCH_QUERY", "AI Engineer India")


def linkedin_login(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.uniform(2,5))
    driver.find_element(By.ID, "username").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(random.uniform(2,5))


def collect_profiles(driver, limit=50):
    profiles = set()
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={SEARCH_QUERY.replace(' ', '%20')}"
    driver.get(search_url)
    time.sleep(random.uniform(2,5))

    scrolls = max(1, limit // 10)  # rough estimate: ~10 profiles per scroll
    for _ in range(scrolls):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(random.uniform(2,5))
        links = driver.find_elements(By.XPATH, "//a[contains(@href, '/in/')]")
        for link in links:
            url = link.get_attribute("href")
            if url and "/in/" in url and "miniProfile" not in url:
                profiles.add(url.split("?")[0])
        if len(profiles) >= limit:
            break
        time.sleep(random.uniform(2,5))

    return list(profiles)[:limit]


def collect_from_selenium(limit=50, out_path="data/profiles.jsonl"):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    try:
        linkedin_login(driver)
        profiles = collect_profiles(driver, limit=limit)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            for p in profiles:
                f.write(json.dumps({"url": p}) + "\n")

        print(f"[collector] Found {len(profiles)} profiles. Saved → {out_path}")
        return [{"url": p} for p in profiles]  # return for use in main collector

    finally:
        driver.quit()


if __name__ == "__main__":
    collect_from_selenium()
