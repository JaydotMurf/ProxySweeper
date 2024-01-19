from bs4 import BeautifulSoup
from colored import Fore, Back, Style
import requests
import threading
import queue
import re

def get_proxies(file_path):
    with open(file_path) as f:
        proxies = f.read().split('\n')
        return [p for p in proxies if re.match(r'^\d+\.\d+\.\d+\.\d+:\d+$', p)]

def validate_proxy(proxy, q, valid_proxies, lock):
    IP_INFO_URL = 'http://ipinfo.io/json'
    try:
        res = requests.get(IP_INFO_URL, proxies={'http': proxy, 'https': proxy}, timeout=5)
        if res.status_code == 200:
            with lock:
                valid_proxies.append(proxy)
    except requests.exceptions.RequestException:
        pass
    finally:
        q.task_done()

def main():
    proxies = get_proxies('free_proxies.txt')
    q = queue.Queue()
    valid_proxies = []
    lock = threading.Lock()

    for proxy in proxies:
        q.put(proxy)

    for _ in range(min(10, len(proxies))):
        threading.Thread(target=lambda: validate_proxy(q.get(), q, valid_proxies, lock)).start()

    q.join()
    print("Valid Proxies:", valid_proxies)

if __name__ == "__main__":
    main()
