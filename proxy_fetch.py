from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from colored import Fore, Back

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
        EC.visibility_of_element_located((By.XPATH, "//textarea[@class='form-control']"))
        )
    assert text_area, "Failed to find text area containing proxies"

    print(f'{Fore.GREEN}Successfully gathered proxy IP addresses')
    return text_area.text
