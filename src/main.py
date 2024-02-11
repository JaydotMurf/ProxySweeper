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


def run_proxy_sweeper():
    free_proxy_list_url = "https://free-proxy-list.net/"
    proxies_file_path = "proxies.txt"
    valid_proxies_file_path = "valid_proxies.txt"

    # Initialize WebDriver
    driver = init_webdriver()

    try:
        # Fetch proxies, validate them, and write to files
        proxies = scrape_proxies(driver, free_proxy_list_url)
        write_proxies_to_file(proxies, proxies_file_path)
        valid_proxies = validate_proxies(proxies_file_path)
        write_proxies_to_file(valid_proxies, valid_proxies_file_path)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    run_proxy_sweeper()
