from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from proxy_fetch import get_unvalidated_proxies  
from file_operations import write_proxies_to_file

if __name__ == "__main__":
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()
    FREE_PROXY_LIST_URL = 'https://free-proxy-list.net/'
    driver.get(FREE_PROXY_LIST_URL)

    # Fetch proxies and write them to a file
    try:
        proxies = get_unvalidated_proxies(driver)
        write_proxies_to_file(proxies, 'proxies.txt')
    finally:
        driver.quit()
