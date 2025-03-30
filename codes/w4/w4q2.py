import requests
from bs4 import BeautifulSoup
def get_movies():
    url = "https://www.imdb.com/search/title/?user_rating=5,8"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    #print(response.text)
    soup = BeautifulSoup(response.text, "lxml")
    movies = []

    for item in soup.find_all("div", class_="lister-item-content"):
        title_tag = item.find("h3", class_="lister-item-header").find("a")
        year_tag = item.find("span", class_="lister-item-year")
        rating_tag = item.find("div", class_="ratings-bar")

        if title_tag and year_tag and rating_tag:
            title = title_tag.text.strip()
            movie_id = title_tag["href"].split("/")[2]  # Extract IMDb ID from the URL
            year = year_tag.text.strip("()")
            rating = rating_tag.find("strong").text if rating_tag.find("strong") else "N/A"

            movies.append({
                "id": movie_id,
                "title": title,
                "year": year,
                "rating": rating
            })
    print(movies)
    return movies

get_movies()