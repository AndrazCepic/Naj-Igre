import time
from threading import Thread
import os
import requests
from bs4 import BeautifulSoup

home_url = 'https://www.metacritic.com/browse/games/score/userscore/all/all/filtered?sort=desc'
page_count = 50
main_pages_dir = "main_pages"

# GET headers
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
headers = {'User-Agent' : user_agent}

potential_fail_urls = []


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
        if url not in potential_fail_urls:
            potential_fail_urls.append(url)
            with open("potential_misses.txt", "w") as f:
                f.write("FOR: " + url + " ERROR: " + e + "\n")   

    return content.text if not content == None else None


def save_str_to_file(text, dir, file_name):
    path = os.path.join(dir, file_name)
    os.makedirs(dir, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)

def save_all_main_pages(start=0):
    """ Funciton saves all the pages we need for the analysis"""
    page_num = start
    while page_num in range(0, page_count):
        html_str = download_url_to_html_string(main_page_url(page_num))
        time.sleep(2)

        # Retry the request if it fails
        if html_str == None:
            continue

        save_str_to_file(html_str, "main_pages", "page_" + str(page_num) + ".html")
        page_num += 1 


def read_file_to_str(dir, file_name):
    path = os.path.join(dir, file_name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_game_links(num_page):
    """ Function extracts the suffixes for the links to the corresponding game pages. """

    links = []
    html = read_file_to_str("main_pages", "page_" + str(num_page) + ".html")
    soup = BeautifulSoup(html, "lxml")

    # The first item (has special class name)
    first_item = soup.find_all("li", class_="product game_product first_product")[0]
    links.append(first_item.a.attrs["href"])

    for item in soup.find_all("li", class_="product game_product"):
        links.append(item.a.attrs["href"])

    # The last item (has special class name)
    last_item = soup.find_all("li", class_="product game_product last_product")[0]
    links.append(last_item.a.attrs["href"])

    return links


def save_game_pages(games, begin, end):
    for i in range(begin, end):
        succ = False
        titles = games[i].split("/")
        file_name = titles[-1] + "_" + titles[-2] + ".html" 
        while not succ:
            html_str = download_url_to_html_string("https://www.metacritic.com" + games[i] + "/details")
            time.sleep(2)

            # Retry the request if it fails
            if html_str != None:
                save_str_to_file(html_str, "game_pages", file_name)
                succ = True


class GameScrapThread (Thread):
    def __init__(self, thread_id, games, begin, end):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.begin = begin
        self.end = end
        self.games = games

    def run(self):
        save_game_pages(self.games, self.begin, self.end)

def main():
    #save_all_main_pages(10)

    #with open("link_list.txt", "w") as f:
    #    for i in range(page_count):
    #        links = extract_game_links(i)
    #        for link in links:
    #            f.write(link + "\n")

    # Download the specific game pages on 4 threads
    list_str = ""
    with open("link_list.txt", "r") as f:
        list_str = f.read()

    games = list_str.split("\n")

    size = int(len(games) / 4)
    threads = [GameScrapThread(i, games, i * size, (i + 1) * size) for i in range(4)]
    for i in range(4):
        threads[i].start()

if __name__ == '__main__':
    main()
