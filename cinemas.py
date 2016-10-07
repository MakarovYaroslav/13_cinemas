import requests
from bs4 import BeautifulSoup
import re


def fetch_afisha_page():
    afisha_link = 'http://www.afisha.ru/msk/schedule_cinema/'
    afisha_page = requests.get(afisha_link)
    return afisha_page.content


def parse_afisha_list(raw_html):
    movie_and_cinemas = {}
    soup = BeautifulSoup(raw_html, 'lxml')
    movies = soup.find_all('div', "object s-votes-hover-area collapsed")
    for movie in movies:
        table = movie.find('table')
        table_body = table.find('tbody')
        cinemas = table_body.find_all('tr')
        movie_name = movie.find('h3').text
        cinema_count = len(cinemas)
        movie_and_cinemas[movie_name] = cinema_count
    return movie_and_cinemas


def fetch_movie_info(movie_title):
    r = requests.get(
        'https://www.kinopoisk.ru/index.php?first=no&what=&kp_query=%s'
        % movie_title
    )
    soup = BeautifulSoup(r.content, 'lxml')
    searched_film = soup.find('div', "element most_wanted")
    rating_div = searched_film.find('div', re.compile('^rating'))
    if rating_div is not None:
        rating_title = rating_div['title']
        rating_and_count = []
        rating_and_count = rating_title.split(' ')
        rating = rating_and_count[0]
        rating_count = rating_and_count[1]
        return (rating, rating_count)
    else:
        return (0, 0)


def output_movies_to_console(movies, count_to_output):
    l = lambda x: x[1]
    sorted_movies = sorted(movies.items(), key=l, reverse=True)
    if count_to_output > len(sorted_movies):
        count_to_output = len(sorted_movies)
    for movie_number in range(count_to_output):
        print(sorted_movies[movie_number][0])


if __name__ == '__main__':
    film_count = input('Введите количество фильмов, которые нужно вывести:')
    movies_with_rating = {}
    movies = parse_afisha_list(fetch_afisha_page())
    for movie in movies.keys():
        rating = fetch_movie_info(movie)[0]
        if rating != '':
            movies_with_rating[movie] = float(rating)
        else:
            movies_with_rating[movie] = 0
    print("Самые классные фильмы (по рейтингу):")
    output_movies_to_console(movies_with_rating, int(film_count))
