# coding:utf-8

from multiprocessing import connection
from unittest import main
from pprint import pprint
from getpass import getpass
from progress.bar import Bar 

import pandas as pd
import pycld2 as cld2
import time
import argparse

import db_helper
import data_scrape
import data_proc
import linker


limit = 2
r_level = 0
url_limit = 5

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--search", action="store_true")
options = parser.parse_args()
if options.search:
    db_helper.search_module()
    exit()

def main():
    bar = Bar("Running : Scrape, Process, Injection")

    root_links = linker.seed_links("link-seed-test.txt")
    for links in root_links:
        linker.get_links(links)

    url_list = linker.seed_links("links-data.txt")
    for url in url_list:
        # scrape_text(url)
        scrapedText = data_proc.processText(data_scrape.scrape_text(url))
        bar.next()
        # print("\nURL : " + url + "Data :" + scrapedText)
        db_helper.inject_data(url, scrapedText)
        bar.next()
    bar.finish()

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
