import urllib.request as request
from bs4 import BeautifulSoup

# Cyclone info base url
CYCLONE_INFO_URL = "http://rammb.cira.colostate.edu/products/tc_realtime/index.asp"
# Cyclone track history and forecast data
CYCLONE_DETAIL_URL = "https://rammb-data.cira.colostate.edu/tc_realtime/storm.asp?storm_identifier="


def get_cyclone_detail_url(cyclone_id):
    return CYCLONE_DETAIL_URL + cyclone_id


def fetch_html_content(url, attrs1, element, attrs2=None):
    page = request.urlopen(url)
    soup = BeautifulSoup(page, features="html.parser")
    return soup.body.find("div", attrs=attrs1).find_all(element, attrs=attrs2)


def fetch_cyclones_info_page():
    return fetch_html_content(CYCLONE_INFO_URL, {"id": "content"}, "div", {
        "class": "basin_storms"})


def fetch_cyclone_details_page(cyclone_id):
    return fetch_html_content(get_cyclone_detail_url(cyclone_id), {"class": "text_product_wrapper"}, "h3")
