from bs4 import BeautifulSoup as soup


def grab_movie_ids(raw_html, logger):
    movie_id_list = []
    ids = soup(raw_html, "html.parser").findAll("a", {
        "class": "list-group-item list-group-item-action flex-column align-items-start"})
    for movie_id in ids:
        movie_id_list.append(movie_id['href'].replace("/movies/", ""))
    logger.info("Total id's found --> " + str(len(movie_id_list)))
    return movie_id_list


def grab_movie_name(raw_html):
    movies = soup(raw_html, "html.parser").findAll("h4", {"class": "card-title"})
    movie = movies[0].text
    return movie


def grab_movie_release_year(raw_html):
    movie_year_list = soup(raw_html, "html.parser").findAll("div", {"class": "col col-md-5 col-lg-5"})
    movie_year = movie_year_list[0].small.text.replace("Release Year - ", "")
    return movie_year


def grab_movie_quote_tags(raw_html):
    movie_tags_list = []
    movie_tags = soup(raw_html, "html.parser").findAll("h6")
    for movie_tag in movie_tags:
        if "Tags:" in movie_tag:
            movie_tags_list.append(movie_tag.span.text)
    return movie_tags_list


def grab_quote_author(raw_html):
    quote_author_list = []
    authors = soup(raw_html, "html.parser").findAll("span", {"class": "badge badge-primary ml-2"})
    for author in authors:
        quote_author_list.append(author.text)
    authors2 = soup(raw_html, "html.parser").findAll("span", {"class": "small"})
    for author2 in authors2:
        if author2.text == "Unknown":
            quote_author_list.append("Unknown")
    return quote_author_list


def grab_movie_quotes(raw_html):
    movie_quotes_list = []
    quotes = soup(raw_html, "html.parser").findAll("h5", {"class": "card-title"})
    for quote in quotes:
        movie_quotes_list.append(quote.text)
    return movie_quotes_list
