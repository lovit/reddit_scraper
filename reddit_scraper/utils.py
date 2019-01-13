import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from time import gmtime, strftime


def now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_soup(url, headers=None):
    if headers is None:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.text
    page = BeautifulSoup(html, 'lxml')
    return page

doublespace_pattern = re.compile('\s+')
lineseparator_pattern = re.compile('\n+')

def normalize_text(text):
    text = text.replace('\t', ' ')
    text = text.replace('\r', ' ')
    text = lineseparator_pattern.sub('\n', text)
    text = doublespace_pattern.sub(' ', text)
    return text.strip()

def unixtime_to_datetime(t):
    return datetime.fromtimestamp(t)

def strf_to_datetime(strf, form='%Y-%m-%d %H-%M-%S'):
    return datetime.strptime(strf, form)