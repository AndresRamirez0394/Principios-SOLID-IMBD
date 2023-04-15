import requests
import re
import csv
from bs4 import BeautifulSoup

#downloads data from URL and returns the HTML contents as a string
def download_movies(url: str) -> str:
    response = requests.get(url)
    return response.text

#parses the content from the URL and extracts the information as a list.
def parse_info(movie_data: str) -> dict:
    soup = BeautifulSoup(movie_data, 'lxml')
    movies = soup.select('td.titleColumn')
    links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
    crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
    votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

    movie_list = []
       # Iterating over movies to extract
    # each movie's details
    for index in range(0, len(movies)):
        # Separating movie into: 'place',
        # 'title', 'year'
        movie_string = movies[index].get_text()
        movie = (' '.join(movie_string.split()).replace('.', ''))
        movie_title = movie[len(str(index)) + 1:-7]
        year = re.search('\((.*?)\)', movie_string).group(1)
        place = movie[:len(str(index)) - (len(movie))]

        data = {"movie_title": movie_title,
                "year": year,
                "place": place,
                "star_cast": crew[index],
                "rating": ratings[index],
                "vote": votes[index],
                "link": links[index],
                "preference_key": index % 4 + 1}
        movie_list.append(data)

    return movie_list

#writes the movie info to a CSV file
def write_movies_csv(movie_list: list, csv_file_path: str):
    fields = ["preference_key", "movie_title", "star_cast", "rating", "year", "place", "vote", "link"]
    with open(csv_file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for movie in movie_list:
            writer.writerow({movie})

#url can be changed to access other movie databases.
def main():
    url = 'http://www.imdb.com/chart/top'
    movie_data = download_movies(url)
    movie_list = parse_info(movie_data)
    write_movies_csv(movie_list, "movie_results.csv")



