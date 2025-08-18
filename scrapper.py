# scraper.py (Final Version - Grabbing Body Text)

import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
    raise ValueError("LINKEDIN_EMAIL and LINKEDIN_PASSWORD must be set in the .env file")

def get_profile_data(profile_url: str) -> str:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(40)

    try:
        print("Navigating to login page...")
        driver.get("https://www.linkedin.com/login")
        
        wait = WebDriverWait(driver, 20)
        
        print("Entering username...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(LINKEDIN_EMAIL)
        
        print("Entering password...")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(LINKEDIN_PASSWORD)
        
        print("Clicking submit...")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        print("Waiting for successful login confirmation...")
        wait.until(EC.presence_of_element_located((By.ID, "global-nav-search")))
        print("Login successful.")
        
        print(f"Navigating to profile: {profile_url}")
        driver.get(profile_url)
        
        print("Waiting for profile page's main headline (h1) to load...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        
        print("Scrolling page to load content...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print("Extracting page content...")
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        # --- THIS IS THE FINAL CHANGE ---
        # Instead of a specific <main> tag, we grab the whole <body>
        # which is guaranteed to exist. The AI can handle the extra text.
        body_content = soup.find("body")
        if body_content:
            print("Scraping successful.")
            return body_content.get_text(separator="\n", strip=True)
        
        print("Could not find body content of the profile.")
        return "Could not find body content of the profile."

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        driver.save_screenshot("debug_screenshot.png")
        print("Saved a screenshot to debug_screenshot.png")
        return f"Error scraping profile: {e}"
    finally:
        print("Closing browser.")
        driver.quit()

# ADD THIS NEW FUNCTION TO THE BOTTOM OF scraper.py

# REPLACE the old search_for_prospects function in scrapper.py with this one.

# REPLACE the search_for_prospects function in scrapper.py with this DEBUGGING version.

# REPLACE the search_for_prospects function in scrapper.py with this FINAL version.

def search_for_prospects(job_title: str, location: str, max_results: int = 5) -> list[str]:
    """
    Performs a LinkedIn search for people and returns a list of profile URLs.
    This is the final, most robust version based on direct HTML inspection.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Adding a common user-agent can sometimes help avoid detection
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Give it a generous timeout
    wait = WebDriverWait(driver, 30)

    try:
        print("--- Prospect Search Initiated ---")
        driver.get("https://www.linkedin.com/login")
        
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(LINKEDIN_EMAIL)
        
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(LINKEDIN_PASSWORD)
        
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        wait.until(EC.presence_of_element_located((By.ID, "global-nav-search")))
        print("Login successful for search.")

        search_keywords = f"{job_title} {location}"
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_keywords.replace(' ', '%20')}"
        print(f"Navigating to search URL: {search_url}")
        driver.get(search_url)

        # --- FINAL KEY CHANGE #1: The Wait Condition ---
        # We wait for the main list of search results to appear.
        print("Waiting for search results list to load...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-results-container")))
        print("Search results page loaded.")
        time.sleep(3) # Extra moment for all elements to render

        # --- FINAL KEY CHANGE #2: The Link Finder XPath ---
        # This XPath is built based on the HTML you provided.
        # It finds the span with the person's name inside, then gets the parent link (the <a> tag).
        profile_links = driver.find_elements(By.XPATH, "//span[contains(@class, 'entity-result__title-text')]//a")
        
        profile_urls = []
        for link in profile_links:
            url = link.get_attribute("href")
            if url and "/in/" in url:
                clean_url = url.split('?')[0]
                if clean_url not in profile_urls:
                    profile_urls.append(clean_url)
                    if len(profile_urls) >= max_results:
                        break
        
        if not profile_urls:
            print("Could not find profile links with the primary XPath. Trying a fallback...")
            # Fallback XPath in case the primary one fails
            profile_links = driver.find_elements(By.XPATH, "//a[@data-test-app-aware-link and contains(@href, '/in/')]")
            for link in profile_links:
                url = link.get_attribute("href")
                if url and "/in/" in url:
                    clean_url = url.split('?')[0]
                    if clean_url not in profile_urls:
                        profile_urls.append(clean_url)
                        if len(profile_urls) >= max_results:
                            break

        print(f"Found {len(profile_urls)} prospect URLs: {profile_urls}")
        return profile_urls

    except Exception as e:
        print(f"An error occurred during prospect search: {e}")
        driver.save_screenshot("debug_search_screenshot.png")
        return []
    finally:
        print("--- Prospect Search Finished ---")
        driver.quit()