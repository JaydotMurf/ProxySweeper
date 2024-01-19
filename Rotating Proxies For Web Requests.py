from colored import Fore, Back, Style 
import requests
import threading
import queue
import re

def read_proxies(file_path):
    assert file_path, "File path for proxies is not provided"
    with open(file_path) as f:
        proxies = f.read().split('\n')
        valid_proxies = [p for p in proxies if re.match(r'^\d+\.\d+\.\d+\.\d+:\d+$', p)]
    assert valid_proxies, "No valid proxies found in the file"
    return valid_proxies

q = queue.Queue()
valid_proxies = []

proxies = read_proxies('free_proxies.txt')
for p in proxies:
    q.put(p)

assert not q.empty(), "Queue is empty after loading proxies"

IP_INFO_URL = 'https://ipinfo.io/json'
MAX_TRIES = 3  # Maximum number of tries for each proxy

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        for attempt in range(MAX_TRIES):
            try:
                res = requests.get(IP_INFO_URL, proxies={'http': proxy, 'https': proxy})
                assert res, "Failed to get a response using proxy: " + proxy
                if res.status_code == 200:
                    print(f"Valid proxy: {proxy}")
                    break
            except Exception as e:
                if attempt < MAX_TRIES - 1:
                    continue
                else:
                    print(f"Failed proxy {proxy} after {MAX_TRIES} attempts: {e}")
                    break
        q.task_done()

for _ in range(10):
    threading.Thread(target=check_proxies).start()
