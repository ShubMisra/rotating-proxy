import requests
import random
import time
from bs4 import BeautifulSoup as bs

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # request and grab content
    soup = bs(requests.get(url).content, 'html.parser')
    # to store proxies
    proxies = []
    for row in soup.find("table", attrs={"class": "table-striped"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(str(ip) + ":" + str(port))
        except IndexError:
            continue
    return proxies

url = "http://httpbin.org/ip"
proxies = get_free_proxies()

start_time = time.time()

for i in range(len(proxies)):
    # Printing request number
    print("Request Number: " + str(i + 1))

    # Get the current proxy
    proxy = proxies[i]

    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        print(response.json())
    except:
        # If the proxy IP is not available
        print("Not Available")

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Generate a random interval between 1 and 10 minutes
    random_interval = random.randint(60, 600)

    # If the elapsed time exceeds the random interval, rotate to the next proxy
    if elapsed_time >= random_interval:
        start_time = time.time()
        if i < len(proxies) - 1:
            print("Rotating proxy...")
        else:
            print("No more proxies available.")
