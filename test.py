from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

req = Request("https://en.wikipedia.org/wiki/Python_(programming_language)")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "html.parser")

html_text = soup.get_text()

f = open("html_text.txt", "w")         # Creating html_text.txt File

for line in html_text:
	f.write(line)

f.close()