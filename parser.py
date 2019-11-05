import os
import csv
from bs4 import BeautifulSoup


# Reading the generated list of games
list_str = ""
with open("link_list.txt", "r") as f:
    list_str = f.read()
game_links = list_str.split("\n")


def extract_title(soup, game_link):
    for tag in soup.find_all("a"):
        if tag.attrs["href"] == game_link:
            return tag.text


def extract_platform(soup):
    tag = soup.find("span", class_="platform")
    children = tag.find_all("a")
    if len(children) == 0:
        return tag.text
    else: 
        return children[0].text


def extract_date(soup):
    tag = soup.find("li", class_="summary_detail release_data")
    return tag.find("span", class_="data").text


def extract_publisher(soup):
    tag = soup.find("li", class_="summary_detail publisher")
    return tag.find("span", class_="data").a.text

def extract_dev(soup):
    tag = soup.find("li", class_="summary_detail publisher")
    return tag.find("span", class_="data").a.text


def extract_mscore(soup):
    pass


def extract_uscore(soup):
    pass


def extract_esrb(soup):
    pass


def extract_genres(soup):
    pass


def extract_game_data(game_link):
    game_data = {}

    # Reading the HTML string
    html = None
    try:
        with open(game_link + ".html", "r") as f:
            html = f.read()
    except Exception as e:
        print(e)
        return None
    
    soup = BeautifulSoup(html, "lxml")

    # Extracting the data
    game_data["title"] = extract_title(soup, game_link)
     