from constants import links_constants


def get_year_url(year):
    return links_constants.movies_by_year_url + year


def get_movie_url(movie_id):
    return links_constants.movies_details_url + movie_id
