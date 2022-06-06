import urllib.request 
import requests

from progress.bar import Bar 
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_links(url):
    bar = Bar('Linker - Scrape Running')
    # response = requests.get(url)

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(url)

    data = response.text
    soup = BeautifulSoup(data, 'lxml')

    links = []
    for link in soup.find_all('a'):
        bar.next()
        link_url = link.get('href')

        if link_url is not None and link_url.startswith('http'):
            links.append(link_url + '\n')
    
    link_set = set(links)
    createUnitDict(url, link_set)
    bar.next()
    write_to_file(link_set)


    bar.finish()
    return links

def createUnitDict(key, value):
    link_dict = {key : set(value)}
    # pprint(link_dict)

def write_to_file(link_set):
    with open('links-data.txt', 'a') as f:
        f.writelines(link_set)

def seed_links(file):
    bar = Bar('Linker - Seeder Running')

    url_list = []
    with open(file) as f:
        lines = f.readlines()

        for line in lines:
            url_list.append(line)
            bar.next()
        url_list = list(map(lambda x:x.strip(), url_list))
        
        bar.finish()
        return url_list
