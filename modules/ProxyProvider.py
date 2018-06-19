import logging
import random
import threading
import requests
import ujson

from modules.Proxy import Proxy

logger = logging.getLogger()


class ProxyProvider:
    def __init__(self, min_proxies=200):
        self._bad_proxies = {}
        self._minProxies = min_proxies
        self.lock = threading.RLock()

        self.get_list()

    def get_list(self):
        logger.debug("Getting proxy list")
        #r = requests.get("http://114.215.99.158:8080/Step/", timeout=10)
        #r = requests.get("https://jsonblob.com/api/jsonBlob/e0ad6c9a-a1f9-11e7-a649-b1a0b98a167c", timeout=10)
        #r = requests.get("https://jsonblob.com/api/jsonBlob/4f177512-ac39-11e7-a12e-11742358a0f9", timeout=10)        
        #proxies = ujson.decode(r.text)
        with open("E:\mobike-crawler\modules\ip.json",'r') as load_f:
            proxies = ujson.load(load_f)
        logging.warning("Got %s proxies", len(proxies))
        self._proxies = list(map(lambda p: Proxy(p), proxies))

    def pick(self):
        with self.lock:
            self._proxies.sort(key = lambda p: p.score, reverse=True)
            proxy_len = len(self._proxies)
            max_range = 50 if proxy_len > 50 else proxy_len
            proxy = self._proxies[random.randrange(1, max_range)]
            proxy.used()

            return proxy

    def count(self):
        with self.lock:
            return len(self._proxies)

if __name__ == "__main__":
    provider = ProxyProvider()
    print(provider.pick().url)
