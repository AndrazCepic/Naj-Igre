import os
import csv
from bs4 import BeautifulSoup


def extract_title(soup, game_link):
    for tag in soup.find_all("a"):
        if tag.attrs["href"] == game_link:
            return tag.text.strip()


def extract_platform(soup):
    tag = soup.find("span", class_="platform")
    children = tag.find_all("a")
    if len(children) == 0:
        return tag.text.strip()
    else: 
        return children[0].text.strip()


def extract_date(soup):
    tag = soup.find("li", class_="summary_detail release_data")
    date = tag.find("span", class_="data").text.strip().split(",")
    date = [entry.strip() for entry in date]
    substrs = [substr.strip() for t in date for substr in t.split(" ")]
    return "_".join(substrs)


def extract_publisher(soup):
    tag = soup.find("li", class_="summary_detail publisher")
    return tag.find("span", class_="data").a.text.strip()


def extract_dev(soup):
    for tag in soup.find_all("tr"):
        if tag.find("th") != None: 
            if tag.find("th").text == "Developer:":
                return tag.find("td").text.strip()


def extract_mscore(soup):
    tag = soup.find("div", class_="metascore_wrap feature_metascore")
    if tag.a == None or tag.a.div == None:
        return "TBD"

    return tag.a.div.span.text.strip()


def extract_uscore(soup):
    tag = soup.find("div", class_="userscore_wrap feature_userscore")
    return tag.a.div.text.strip()


def extract_esrb(soup):
    for tag in soup.find_all("tr"):
        if tag.find("th") != None:
            if tag.find("th").text == "Rating:":
                return tag.find("td").text.strip()


def extract_genres(soup):
    for tag in soup.find_all("tr"):
        if tag.find("th") != None:
            if tag.find("th").text == "Genre(s):":
                genres = tag.find("td").text.strip().split(",")
                return [genre.strip() for genre in genres]


def extract_game_data(game_link):
    game_data = {}
    genres = {}

    # Reading the HTML string
    html = None
    try:
        link_details = game_link.split("/")
        prefix = link_details[-1] + "_" + link_details[-2]
        with open("game_pages/" + prefix + ".html", "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(e)
        return None
    
    soup = BeautifulSoup(html, "lxml")

    # Extracting the data
    try:
        game_data["title"] = extract_title(soup, game_link)
        game_data["platform"] = extract_platform(soup)
        game_data["date"] = extract_date(soup)
        game_data["publisher"] = extract_publisher(soup)
        game_data["developer"] = extract_dev(soup)
        game_data["metascore"] = extract_mscore(soup)
        game_data["user_score"] = extract_uscore(soup)
        game_data["esrb"] = extract_esrb(soup)
        genres = extract_genres(soup)
    except Exception as e:
        print(e)
        print("GAME FAILED: " + game_link)
        return None
 
    return game_data, genres


def write_csv(dicts, fields, file_name):
    path = os.path.join("data", file_name)
    os.makedirs("data", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in dicts:
            writer.writerow(row)


# Reading the generated list of games
list_str = ""
with open("link_list.txt", "r", encoding="utf-8") as f:
    list_str = f.read()
game_links = list_str.split("\n")



# Writing to CSV files (game csv and genres csv) 
games = []
genres = []
for game_link in game_links:
    pair = extract_game_data(game_link)
    if pair == None:
        continue

    game_data, game_genres = pair
    games.append(game_data)
    
    # Setting up the genres dict
    # During testing multiple occurances of the same genre would appear,
    # hence the guard was required
    done_genres = []
    for genre in game_genres:
        if genre in done_genres:
            continue
        genres.append({"title" : game_data["title"], 
                        "platform" : game_data["platform"],
                        "genre" : genre})
        done_genres.append(genre)
games.sort(key=lambda game: game["title"])
genres.sort(key=lambda game: game["title"])
game_fields = ["title",
                     "platform",
                     "date",
                     "publisher",
                     "developer",
                     "metascore",
                     "user_score",
                     "esrb"]
genre_fields = ["title", "platform", "genre"]
write_csv(games, game_fields, "games.csv")
write_csv(genres, genre_fields, "genres.csv")