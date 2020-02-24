###################################################################################
#
#   file makes simple convenience method for getting a logger instance
#
###################################################################################
import logging


def logger_factory(file_name,
                   logger_name=__name__,
                   format_string='%(levelname)s : %(asctime)s : %(name)s : %(message)s',
                   print_stream=True,
                   logging_level='INFO') -> logging.Logger:
    """
    returns a configured logger object
    :param file_name:
    :param logger_name:
    :param format_string:
    :param print_stream:    set this true to stream logger output to console
    :param logging_level:
    :return: pre configured logger object
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, logging_level))

    formatter = logging.Formatter(fmt=format_string, datefmt='%m/%d/%Y %I:%M:%S %p')

    if not logger.hasHandlers():
        file_handler = logging.FileHandler(filename=file_name)
        file_handler.setLevel(getattr(logging, logging_level))
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        if print_stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

    return logger
