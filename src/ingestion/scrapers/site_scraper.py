# scrapers/site_scraper.py

import time
from typing import List, Dict
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.selenium_setup import get_chrome_driver
from utils.logger import get_logger

logger = get_logger(__name__)

def scrape_website(site_config: dict) -> List[Dict]:
    """
    Scrapes articles from a single website based on the provided configuration.
    Returns a list of article dicts with keys like 'title', 'url', etc.
    """
    driver = None
    articles = []

    try:
        driver = get_chrome_driver(headless=True)
        driver.get(site_config["start_url"])
        time.sleep(2)  # give the page some time to load, adjust as needed

        while True:
            # 1. Find article containers
            article_elements = driver.find_elements_by_xpath(site_config["article_container_xpath"])
            for element in article_elements:
                try:
                    title_el = element.find_element_by_xpath(site_config["title_xpath"])
                    link_el = element.find_element_by_xpath(site_config["link_xpath"])

                    title_text = title_el.text.strip()
                    article_url = link_el.get_attribute("href")

                    articles.append({
                        "title": title_text,
                        "url": article_url,
                    })
                except NoSuchElementException:
                    # Some articles might not have the exact structure
                    logger.warning("Missing element in article container.")
                    continue

            # 2. Check if pagination is enabled
            if site_config.get("pagination_enabled", False):
                try:
                    next_page_button = driver.find_element_by_xpath(site_config["pagination_xpath"])
                    next_page_url = next_page_button.get_attribute("href")
                    if not next_page_url:
                        # If there's no href, break out
                        break
                    driver.get(next_page_url)
                    time.sleep(2)
                except NoSuchElementException:
                    # No more pages
                    break
            else:
                break  # pagination not enabled, so just one pass

        return articles

    except TimeoutException as e:
        logger.error(f"TimeoutException scraping {site_config['name']}: {e}")
    except Exception as e:
        logger.error(f"Unknown error scraping {site_config['name']}: {e}", exc_info=True)
    finally:
        if driver:
            driver.quit()

    return articles