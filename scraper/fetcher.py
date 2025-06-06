import requests
from .config import URL, HEADERS

def fetch_html():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    return response.text