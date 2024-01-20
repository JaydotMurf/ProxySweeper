from selenium import webdriver
from selenium.webdriver.common.by import By

PROXY = "72.10.160.90:29129" # demo proxy

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

chrome = webdriver.Chrome(options=chrome_options)
chrome.get("http://checkip.amazonaws.com/")

body_text = chrome.find_element(By.TAG_NAME, 'body').text
print(body_text)
chrome.quit()