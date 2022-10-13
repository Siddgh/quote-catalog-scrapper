import pandas as pd
from constants import name_constants
from models import write_to_csv_model


def write_csv(file_name, data_to_write):
    quotes_data = open(file_name, "a")
    quotes_data.write(
        data_to_write.year + "|" + data_to_write.movie + "|" + data_to_write.quote + "|" + data_to_write.author + "|" + data_to_write.tags + "|" + data_to_write.status + "\n")
    quotes_data.close()


def setup_quotes_to_be_written_to_csv(movie, quote, author, tag, year, logger, success_logger, exists_logger):
    logger.info("\nMovie --> " + movie)
    logger.info("Quote found --> " + quote)
    logger.info(" Author --> " + author)
    logger.info("Tags --> " + tag)
    logger.info("Year --> " + year + "\n")
    logger.info("----------------------- Checking if Quote Exists -----------------------\n")
    if not check_if_quote_already_exists(quote):
        data_to_write = write_to_csv_model.CSVWriterModel(year=year, movie=movie,
                                                          quote=quote, author=author,
                                                          tags=tag, status=name_constants.NOT_UPLOADED)
        write_csv(name_constants.csv_file_name, data_to_write)
        logger.info("Quote Added --> " + quote)
        success_logger.info("Movie --> " + movie + " Quote --> " + quote)
    else:
        logger.info("Already Exists --> " + quote)
        exists_logger.info("Movie --> " + movie + " Quote --> " + quote)


def csv_to_data_frame_converter(file_name):
    return pd.read_csv(file_name, delimiter="|", error_bad_lines=False)


def check_if_csv_header_already_exists(file_name):
    has_header = False
    try:
        csv_data_frame = csv_to_data_frame_converter(file_name)
        if len(csv_data_frame.columns) > 2:
            has_header = True
        else:
            has_header = False
    except Exception as e:
        print(e)
    return has_header


def check_if_quote_already_exists(quote):
    csv_data_frame = csv_to_data_frame_converter(name_constants.csv_check_file_name)
    uploaded_quotes_df = csv_data_frame.loc[csv_data_frame[name_constants.quote] == quote]
    if uploaded_quotes_df.empty:
        quote_already_exists = False
    else:
        quote_already_exists = True
    return quote_already_exists
