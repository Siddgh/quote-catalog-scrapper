import datetime
import logging

from constants import name_constants
from models import write_to_csv_model
from utils import csv_utils
from urllib.request import urlopen as uOpen
from utils import string_utils
from utils import crawler_utils


current_year = datetime.datetime.now().year
current_date = str(datetime.date.today())
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def setup_logger(log_filename, log_name, level=logging.INFO):
    handler = logging.FileHandler(log_filename, mode='w')
    handler.setFormatter(formatter)
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def create_csv_header():
    logger.info(
        "----------------------- Starting CSV File Check -----------------------")
    if not csv_utils.check_if_csv_header_already_exists(name_constants.csv_file_name):
        header_data = write_to_csv_model.CSVWriterModel(year=name_constants.year, movie=name_constants.movie,
                                                        quote=name_constants.quote, author=name_constants.author,
                                                        tags=name_constants.tags, status=name_constants.status)
        csv_utils.write_csv(name_constants.csv_file_name, header_data)
        logger.info("CSV File Created with Header")
    else:
        logger.info("CSV File Already Exists")
    logger.info(
        "----------------------- CSV File Check Complete -----------------------\n")


def fetch_movie_quotes_details(uMovieDetail):
    year = crawler_utils.grab_movie_release_year(uMovieDetail)
    movie = crawler_utils.grab_movie_name(uMovieDetail)
    quotes = crawler_utils.grab_movie_quotes(uMovieDetail)
    author = crawler_utils.grab_quote_author(uMovieDetail)
    tags = crawler_utils.grab_movie_quote_tags(uMovieDetail)
    return year, movie, quotes, author, tags


if __name__ == '__main__':

    logger = setup_logger(name_constants.log_file_name +
                          current_date + ".log", 'logger')
    success_logger = setup_logger(
        name_constants.success_logs + current_date + ".log", 'success')
    exists_logger = setup_logger(
        name_constants.existing_logs + current_date + ".log", 'exists')

    create_csv_header()
    for index in reversed(range(name_constants.movies_year_limit, 2004)):
        year = str(index)
        logger.info(
            "----------------------- Fetching URL for Year -----------------------")
        year_url = string_utils.get_year_url(year)
        logger.info("URL --> " + year_url)
        logger.info("Year --> " + year)
        uClient = uOpen(year_url)
        movie_ids = crawler_utils.grab_movie_ids(uClient.read(), logger)
        logger.info("Movie Id's found --> " + ",".join(movie_ids))
        logger.info(
            "----------------------- Fetching URL for Year Complete -----------------------\n")
        for movie_id in movie_ids:
            movie_url = string_utils.get_movie_url(movie_id)
            uMovieDetail = uOpen(movie_url).read()
            movie_name = crawler_utils.grab_movie_name(uMovieDetail)
            logger.info("----------------------- Writing Quotes for Movie " +
                        movie_name + " -----------------------")
            year, movie, quotes, authors, tags = fetch_movie_quotes_details(
                uMovieDetail)
            for numberOfQuotes in range(len(quotes)):
                quote = quotes[numberOfQuotes]
                author = authors[numberOfQuotes]
                tag = tags[numberOfQuotes]
                csv_utils.setup_quotes_to_be_written_to_csv(quote=quote, movie=movie, year=year, author=author, tag=tag,
                                                            logger=logger, success_logger=success_logger,
                                                            exists_logger=exists_logger)
            logger.info(
                "----------------------- Writing Quotes for Movie " + movie_name + " Complete -----------------------\n")
