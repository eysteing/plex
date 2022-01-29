from plexapi.server import PlexServer
import random
import inquirer
from inquirer.themes import GreenPassion
from pprint import pprint

from requests import ReadTimeout

baseurl = 'http://192.168.1.9:32400'
token = 'z2bbh3MJ3pYjJdLcZFDp'
plex = PlexServer(baseurl, token)

# ------- Find Clients -------
clients = [client.title for client in plex.clients()]

plex.library.update()


# ------- MOVIE & TV -------
def video_updater():
    movies_lib = plex.library.section('Movies')
    movies = [video.title for video in movies_lib.search()]
    tv_series_lib = plex.library.section('TV Shows')
    tv_series = [video.title for video in tv_series_lib.search()]
    return movies, tv_series


# ------- Play -------
def play_video(movie, client):
    movie_to_watch = plex.library.section('Movies').get(movie)
    client = plex.client(client)
    client.playMedia(movie_to_watch)


def run_plex_api():
    movies, tv_series = video_updater()
    n_movies = len(movies)
    while True:
        movie_idx = [movies[random.randrange(0, n_movies)] for _ in range(5)]
        movie_idx.append('Or new shuffle? ')
        movie_idx.append('Exit')
        questions_movie = [
            inquirer.List('movie',
                          message="Which movie do you want to see? ",
                          choices=movie_idx,
                          ),
        ]
        answers_movies = inquirer.prompt(questions_movie, theme=GreenPassion())

        if answers_movies["movie"] == 'Exit':
            break
        elif answers_movies["movie"] == 'Or new shuffle? ':
            continue
        else:
            questions_client = [
                inquirer.List('client',
                              message="Which client is watching? ",
                              choices=clients,
                              ),
            ]
            answers_client = inquirer.prompt(questions_client, theme=GreenPassion())
            try:
                play_video(str(answers_movies["movie"]), str(answers_client["client"]))
            except ReadTimeout:
                pass

        # TODO make an updater for the tv_series and movies
