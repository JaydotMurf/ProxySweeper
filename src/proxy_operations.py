import queue
import re
import threading

import requests
from colored import Fore
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_unvalidated_proxies(driver):
    """
    Fetches unvalidated proxy IP addresses from a specific website.

    This function navigates to a website with a list of free proxies,
    clicks on an element to reveal a text area containing proxy IP addresses,
    and then retrieves these addresses.

    Args:
        driver (webdriver): Selenium WebDriver used to interact with the browser.

    Returns:
        str: A string containing proxy IP addresses, each separated by a newline.
    """
    assert driver, "WebDriver instance is required"

    # Using CSS Selector for 'a' element because it has multiple classes
    a_element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".fa.fa-clipboard"))
    )
    assert a_element, "Failed to find clickable element for proxies"

    a_element.click()

    text_area = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//textarea[@class='form-control']")
        )
    )
    assert text_area, "Failed to find text area containing proxies"

    print(f"{Fore.GREEN}Successfully gathered proxy IP addresses")
    return text_area.text


def proxy_validation_worker(q, valid_proxies, lock):
    VALIDATION_URL = "https://ipinfo.io/json"
    while True:
        proxy = q.get()
        if proxy is None:  # Trip value check
            q.task_done()
            break 

        try:
            res = requests.get(VALIDATION_URL, proxies={"http": proxy, "https": proxy})
            if res.status_code == 200:
                print(f"{Fore.GREEN}{proxy}")
                with lock:
                    valid_proxies.append(proxy)
        except requests.exceptions.RequestException:
            pass
        q.task_done()


def validate_proxies(file_path, number_of_workers=10):
    assert file_path, "No file path provided"

    q = queue.Queue()
    valid_proxies = []
    lock = threading.Lock()

    with open(file_path) as f:
        proxies = [p for p in f.read().split("\n") if p.strip()]

    for p in proxies:
        if re.match(r'^\d+\.\d+\.\d+\.\d+:\d+$', p):
            q.put(p)

    # Add a trip value for each worker to indicate the end of the queue
    for _ in range(number_of_workers):
        q.put(None)

    threads = []
    for _ in range(number_of_workers):
        t = threading.Thread(
            target=proxy_validation_worker, args=(q, valid_proxies, lock)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return valid_proxies
