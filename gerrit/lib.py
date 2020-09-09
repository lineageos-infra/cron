import os

import requests
from requests.auth import HTTPBasicAuth

from config import *

print(f"Logging at {LOG_LEVEL}")

def dprint(*args):
    if LOG_LEVEL == "DEBUG":
        print(*args)

class rest:
    auth = HTTPBasicAuth(USERNAME, PASSWORD)

    @classmethod
    def get(cls, url):
        req = requests.get(f"{URL}a{url}", auth=cls.auth)
        dprint(req.status_code, req.text)
        if req.status_code == 200:
            raw = req.text[5:]
            return json.loads(raw)

    @classmethod
    def post(cls, url, j):
        req = requests.post(f"{URL}a{url}", auth=cls.auth, json=j)
        dprint(req.status_code, req.text)
        if req.status_code == 500:
            print(f"Error applying {url}: {req.text}")

    @classmethod
    def put(cls, url, j=None):
        req = requests.put(f"{URL}a{url}", auth=cls.auth, json=j)
        dprint(req.status_code, req.text)
        if req.status_code == 500:
            print(f"Error applying {url}: {req.text}")
