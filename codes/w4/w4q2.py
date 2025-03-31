import requests
from bs4 import BeautifulSoup
import  json
import  re

def get_movies(question):
    pattern = r"rating between\s*(\d+)\s*and\s*(\d+).*?For up to the first\s*(\d+)\s*titles"

    # Search for the pattern in the text
    matches = re.findall(pattern, question, re.IGNORECASE | re.DOTALL)
    min_rating = 5
    max_rating = 8
    max_results = 25
    # If matches are found, extract the values
    if matches:
        min_rating, max_rating, max_results = matches[0]
        print(f"min_rating: {min_rating}")
        print(f"max_rating: {max_rating}")
        print(f"max_results: {max_results}")

    url = f"https://www.imdb.com/search/title/?user_rating={min_rating},{max_rating}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    #print(response.text)
    soup = BeautifulSoup(response.text, "lxml")
    movies = []
    k=0
    for item in soup.find_all("div", class_="ipc-metadata-list-summary-item__c"):
        if(k<int(max_results)):
            title_tag = item.find("div", class_="ipc-title").find("a")

            year_tag = item.find("span", class_="dli-title-metadata-item")
            rating_tag = item.find("span", class_="ipc-rating-star--rating")

            if title_tag and year_tag and rating_tag:
                title = title_tag.text.strip()
                movie_id = title_tag["href"].split("/")[2]  # Extract IMDb ID from the URL
                year = year_tag.text.strip("()")
                rating = rating_tag.text.strip("()")

                movies.append({
                    "id": movie_id,
                    "title": title,
                    "year": year,
                    "rating": rating
                })
                k+=1
    print(json.dumps(movies))
    return movies


