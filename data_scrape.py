import requests
import re

from progress.bar import Bar 
from requests import request
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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
 