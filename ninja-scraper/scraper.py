import urllib.request as request
from bs4 import BeautifulSoup

CYCLONE_INFO_URL = "http://rammb.cira.colostate.edu/products/tc_realtime/index.asp"

page = request.urlopen(CYCLONE_INFO_URL)
soup = BeautifulSoup(page)

x = soup.body.find('div', attrs={'id' : 'content'})

print(x)