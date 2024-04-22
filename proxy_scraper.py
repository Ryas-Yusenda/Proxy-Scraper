import time
from multiprocessing.pool import ThreadPool
import random
import requests

proxy_source_list = [
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


class ProxyScraper:
    """Fetch a fresh list of proxies for usage during runtime."""

    def __init__(self):
        self.proxy_list = []

    def fetch_proxy(self, source):
        try:
            response = requests.get(source, headers=HEADERS, timeout=10)
            return response.text.split()
        except Exception as e:
            print(f"Error fetching from {source}: {e}")
            return []

    def scraper(self, isSave=False):
        try:
            # Fetch proxies in parallel
            with ThreadPool(processes=4) as pool:
                results = pool.map(self.fetch_proxy, proxy_source_list)

            # Flatten the list of lists
            all_proxies = [proxy for sublist in results for proxy in sublist]

            # Remove duplicates
            proxy_set = set(all_proxies)

            for proxy in proxy_set:
                proxyy = {"http": proxy}
                self.proxy_list.append(proxyy)

            # Save in a file txt
            if isSave:
                with open("proxies.txt", "w", encoding="utf-8") as file:
                    for proxy in self.proxy_list:
                        file.write(f"{proxy['http']}\n")

            return self.proxy_list

        except Exception as e:
            print(f"Error: {e}")
            return []

    def select_proxy(self):
        try:
            return random.choice(self.proxy_list)
        except Exception as e:
            print(f"Error: {e}")
            return None


if __name__ == "__main__":
    start_time = time.time()

    proxy_scraper = ProxyScraper()
    proxy_scraper.scraper(True)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total runtime: {elapsed_time:.2f} seconds")

    print(proxy_scraper.select_proxy())
