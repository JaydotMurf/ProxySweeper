from colored import Back
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from file_operations import write_proxies_to_file
from proxy_operations import get_unvalidated_proxies, validate_proxies


def init_webdriver(headless=True):
    """Initializes and returns a Selenium WebDriver."""
    options = Options()
    if headless:
        options.add_argument("--headless")
    try:
        web_driver = webdriver.Chrome(options=options)
        return web_driver
    except WebDriverException as initializing_error:
        print(f"{Back.RED}Error initializing WebDriver: {initializing_error}")
        exit(1)


def scrape_proxies(web_driver, url):
    """Scrapes proxies from the given URL using the provided driver."""
    web_driver.get(url)
    return get_unvalidated_proxies(web_driver)


if __name__ == "__main__":
    FREE_PROXY_LIST_URL = "https://free-proxy-list.net/"

    # Initialize WebDriver
    driver = init_webdriver()

    try:
        # Fetch proxies and write them to a file
        proxies = scrape_proxies(driver, FREE_PROXY_LIST_URL)
        write_proxies_to_file(proxies, "proxies.txt")
        valid_proxies = validate_proxies("proxies.txt")
        write_proxies_to_file(valid_proxies, "valid_proxies.txt")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
