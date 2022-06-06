# coding:utf-8

from multiprocessing import connection
from unittest import main
from bs4 import BeautifulSoup
from pprint import pprint
from getpass import getpass
from progress.bar import Bar 
from mysql.connector import connect, Error

from textblob import TextBlob
from langdetect import detect

import urllib.request 
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
import pycld2 as cld2
import re
import time
import argparse


start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--search", action="store_true")

limit = 2
r_level = 0
url_limit = 5

bar = Bar('Processing')


def init_db():
    connection = connect(
            host="localhost",
            port="8889",
            user="root",
            password="root",
            database="scrapper",
        ) 
    cursor = connection.cursor()
    return connection, cursor

def inject_data(url, data):
    connection, cursor = init_db()

    show_db_query = "SHOW DATABASES"
    inject_text_query = """
    INSERT INTO scrape (url, data_blob)
    VALUES (%s, %s)
    """
    values = (url, data)


    cursor.execute(inject_text_query, values)
    connection.commit()

    for db in cursor:
        print(db)

def search_data(keyword):
    connection, cursor = init_db()

    param = "%{}%".format(keyword)
    search_query = """
    SELECT *
    FROM scrape
    WHERE data_blob LIKE %s
    """

    cursor.execute(search_query, (param,))
    data = cursor.fetchall()

    return data
    # for data in cursor.fetchall():
    #     return data
        # print(data[0])

def search_module():
    keyword = input("Enter keyword to search : ")
    data = search_data(keyword)

    length = len(data)
    print("Rows :: " + str(length))
    for row in data:
        print("############################################################################################################")
        print("ID -> " + str(row[0]))
        print("URL -> " + row[1])
        print("Blob -> \n" + row[2])
        print("Exec Time : ", (time.time() - start_time))
        print("############################################################################################################")



def get_links(url):
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
        url_list = list(map(lambda x:x.strip(), url_list))
        
        return url_list

def scrape_text(url):

    # Get PARAGRAPH TEXTS
    # getting all the paragraphs
    # for para in htmlParse.find_all("p"):
        # print(para.get_text())

    # opening the url for reading
    response = requests.get(url)
    html = response.text

    # parsing the html file
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    cleaned_text = re.sub('\s+',' ',text)

    
    print("\n🟢 URL : " + url + "\n🟢 Data : " + cleaned_text)

    return cleaned_text
    

def validate_language(text):
    validated = False
    validated = isAssamese(handleNoFeature(text))

    return (True if validated else False)

def handleNoFeature(text):
    try:
        res_buffer = detect(text)
    except:
        res_buffer = "other"
    return res_buffer

def isAssamese(param):
    if param == "bn":
        return True
    else:
        return False

def processText(text):
    
    text_stg_1 = " ".join(substr for substr in text.split(" ") if validate_language(substr))
    text_stg_2 = processText_stg_2(text_stg_1)

    print("\n🟢 Procesed Data : " + text_stg_2)

    return text_stg_2

def processText_stg_2(text):
    # print(text)
    return text
    # if "র" in text:
    #     return False
    # else:
    #     return text

options = parser.parse_args()
if options.search:
    search_module()
    exit()

def main():
    

    root_links = seed_links("link-seed-test.txt")
    for links in root_links:
        get_links(links)
    url_list = seed_links("links-data.txt")
    for url in url_list:
        # scrape_text(url)
        scrapedText = processText(scrape_text(url))
        # print("\nURL : " + url + "Data :" + scrapedText)
        inject_data(url, scrapedText)










    # sample = "ভৱেন বৰুৱা"
    # print(validate_language(sample))
    # print(scrape_text("http://www.xophura.net/tag/bhaben-barua"))

    # text = processText(scrape_text("http://www.xophura.net/category/old-assamese"))
    # print(text)
    # inject_data("http://www.xophura.net/tag/bhaben-barua", text)

    # search_data(" তোম")
    # search_module()

    # sample = "সঁফুৰা সঁফুৰা ভৱেন র বৰুৱা|| ১৯৪১- তোমালোকৰ তোমালোকৰ দুখ তোমালোকৰ তোমালোকৰ দুখৰ শিপাবোৰ তোমালোকৰ তোমালোকৰ দুখৰ মাটিবৰ তোমালোকৰ তোমালোকৰ দুখৰ বাবে ৰ’দবোৰ বৰষুণৰ বতাহবোৰ তোমালোকৰ এটা চৰাই মোৰ গীতকো তোমালোকৰ দুখৰ বন্ধু হ’বলৈ উৰুৱাই দিওঁ সিও হোক তোমালোকৰ ক’লা পাত্ৰটোত যিসকলে পান কৰিলা যিসকলে পান কৰিলা বনৰীয়া গছৰ ফলৰ তিতা ৰস ৰাত্ৰিৰ পাত্ৰটোত- বগা পাত্ৰটোত যিসকলে পান কৰিলা যিসকলে পান কৰিলা বনৰীয়া গছৰ ফলৰ তিতা ৰস দিনৰ পাত্ৰটোত- স্থিৰ দৃষ্টিৰে সেইসকলে চাই ৰোৱা ক’লা পাত্ৰটোৰ ভিতৰলৈ বগা পাত্ৰটোৰ ভিতৰলৈ ভীত নহবাঁ ক্লান্ত নহবাঁ হতাশ নহবাঁ তোমালোকৰ তিক্ত শূন্যতাত তোমালোক নিঃস্ব নোহোৱা তোমালোকৰ দুখ তোমালোকৰ শিপাৰোৰ মাটিবোৰ ৰ’দবোৰ বৰষুণবোৰ বতাহবোৰ সকলো তোমালোকৰ তোমালোকৰ দুখৰ ডালত বহি তোমালোকৰ দুখৰ পাতবোৰৰ মাজৰপৰা চৰাইটোৱে শুনাই ৰকঃ তোমালোক নিঃস্ব নোহোৱা তোমালোক নিঃস্ব নোহোৱা সঁফুৰা"
    # processText(sample)

if __name__ == "__main__":
    main()
    































#u = unicode(s, "utf-8")



# def get_all_links(url):
#     global r_level
#     global limit

#     r_level = r_level + 1
#     for link in get_links(url):
#         get_all_links(link)
#         if r_level == limit:
#             print("hola")
#             return
