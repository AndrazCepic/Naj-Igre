import re 
import csv
import os
import json
import requests

home_url = 'https://www.metacritic.com/browse/games/score/userscore/all/all/filtered?sort=desc'
products_per_page = 98
page_count = 10

game_data = {}

main_page_regex = (
    r'<li class="product game_product".*?'
    r'"basic_stat product_title".*?"(?P<game_link>/game.+?)"'
)

game_item_regex = (

)

# GET headers
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
headers = {'User-Agent' : user_agent}


def main_page_url(page_num):
    """ Function takes the number of the page we want
    and returns the URL of the page
    """
    return home_url + '&page=' + str(page_num)


def download_url_to_html_string(url):
    """ Function takes an URL of a page and downloads, 
    then returns the full HTML string it downloaded
    """
    content = None
    try:
        content = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
    return content.text


def save_str_to_file(text, dir, file_name):
    path = os.path.join(dir, file_name)
    os.makedirs(dir, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)


def save_page(url, dir, file_name): 
    """ Function downloads the html string from the url
    and saves the sting to a .html file_name at the specified
    location
    """
    html_str = download_url_to_html_string(url)
    save_str_to_file(html_str, dir, file_name)


def save_all_main_pages():
    """ Funciton saves all the pages we need for the analysis"""
    for page_num in range(5, page_count):
        save_page(main_page_url(page_num), "main_pages", "page_" + str(page_num) + ".html")


def page_to_games(page_html):
    return re.findall(main_page_regex, page_html, re.DOTALL)


def read_html_file_name(dir, file_name):
    path = os.path.join(dir, file_name)
    with open(path, "r", encoding="utf8") as f:
        return f.read()


def write_json(obj, dir, file_name):
    path = os.path.join(dir, file_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)


def parse_games(game_link_list):
    for glink in game_link_list[:5]:
        content = download_url_to_html_string("https://www.metacritic.com" + glink + "/details")
        game_data[]


def main():
    #save_all_main_pages()
    #print(page_to_games(read_html_file("main_pages", "page_0.html")))
    pass

if __name__ == '__main__':
    main()