import re 
import csv
import os
import requests

home_url = 'https://www.metacritic.com/browse/games/score/userscore/all/all/filtered?sort=desc'
products_per_page = 0
page_count = 1

main_page_regex = r'<li class="product game_product".*?"basic_stat product_title".*?"(?P<game_link>/game.+?)"'

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
    try:
        content = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
    return content.text


def save_str_to_file(text, dir, file):
    os.makedirs(dir, exist_ok=True)
    path = os.path.join(dir, file)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)


def save_page(url, dir, file): 
    """ Function downloads the html string from the url
    and saves the sting to a .html file at the specified
    location
    """
    html_str = download_url_to_html_string(url)
    save_str_to_file(html_str, dir, file)


def save_all_main_pages():
    """ Funciton saves all the pages we need for the analysis"""
    for page_num in range(page_count):
        save_page(main_page_url(page_num), "main_pages", "page_" + str(page_num) + ".html")


def page_to_games(page_html):
    return re.findall(main_page_regex, page_html, re.DOTALL)


def read_html_file(dir, file):
    path = os.path.join(dir, file)
    with open(path, "r", encoding="utf8") as f:
        return f.read()





def main():
    # save_all_main_pages()
    count = len(page_to_games(read_html_file("main_pages", "page_0.html")))
    print(count)


if __name__ == '__main__':
    main()