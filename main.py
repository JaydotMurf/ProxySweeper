from colored import Fore, Back
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from proxy_operations import get_unvalidated_proxies, validate_proxies
from file_operations import write_proxies_to_file


def init_webdriver(headless=True):
    """Initializes and returns a Selenium WebDriver."""
    options = Options()
    if headless:
        options.add_argument("--headless")
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException as e:
        print(f"{Back.RED}Error initializing WebDriver: {e}")
        exit(1)


def scrape_proxies(driver, url):
    """Scrapes proxies from the given URL using the provided driver."""
    driver.get(url)
    return get_unvalidated_proxies(driver)


if __name__ == "__main__":
    FREE_PROXY_LIST_URL = "https://free-proxy-list.net/"

    # Initialize WebDriver
    driver = init_webdriver()

    try:
        # Fetch proxies and write them to a file
        proxies = scrape_proxies(driver, FREE_PROXY_LIST_URL)
        write_proxies_to_file(proxies, "proxies.txt")
        valid_proxies = validate_proxies("proxies.txt")
        print("Valid Proxies:", valid_proxies)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
