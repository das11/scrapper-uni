from bs4 import BeautifulSoup
from pprint import pprint
from getpass import getpass
from progress.bar import Bar 
from mysql.connector import connect, Error

from textblob import TextBlob
from langdetect import detect

import urllib.request 
import requests
import pandas as pd
import pycld2 as cld2


limit = 2
r_level = 0
url_limit = 5

bar = Bar('Processing')


def get_links(url):
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')

    links = []
    for link in soup.find_all('a'):
        link_url = link.get('href')

        if link_url is not None and link_url.startswith('http'):
            links.append(link_url + '\n')
    
    link_set = set(links)
    createUnitDict(url, link_set)
    write_to_file(link_set)

    bar.next()
    return links

def createUnitDict(key, value):
    link_dict = {key : set(value)}
    bar.next()
    # pprint(link_dict)

def write_to_file(link_set):
    with open('links-data.txt', 'a') as f:
        f.writelines(link_set)
    bar.next()

def seed_links(file):
    url_list = []
    with open(file) as f:
        lines = f.readlines()

        for line in lines:
            url_list.append(line)
        
        return url_list

def scrape_text(url):
    # opening the url for reading
    response = requests.get(url)
    html = response.text

    # parsing the html file
    soup = BeautifulSoup(html, 'html.parser')
    
    # text = soup.get_text()
    text = "শেৱক"
    print(detect(text))

    # s = text.encode("utf-8")
    # _, _, _, detected_language = cld2.detect(s, returnVectors=True)
    # print(cld2.detect(s, bestEffort=False))

    # getting all the paragraphs
    # for para in htmlParse.find_all("p"):
        # print(para.get_text())

def init_db():
    try:
        with connect(
            host="localhost",
            port="8889",
            user="root",
            password="root",
        ) as connection:
            cursor = connection.cursor()
            inject_data(cursor)
    except Error as e:
        print(e)

def inject_data(cursor):
    show_db_query = "SHOW DATABASES"
    cursor.execute(show_db_query)
    for db in cursor:
        print(db)


if __name__ =="__main__":
    
    # init_db()

    # root_url = 'http://www.xophura.net/'
    # url_list = seed_links("link-seed.txt")
    # for url in url_list:
    #     get_links(url)
    # bar.finish()

    scrape_text("http://www.xophura.net/")
    


    



































# def get_all_links(url):
#     global r_level
#     global limit

#     r_level = r_level + 1
#     for link in get_links(url):
#         get_all_links(link)
#         if r_level == limit:
#             print("hola")
#             return
