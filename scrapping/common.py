import requests
import json
from bs4 import BeautifulSoup

def getPage(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')