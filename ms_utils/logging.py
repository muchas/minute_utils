import logging
import sys


def get_stdout_logger(name, log_level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    formatter = logging.Formatter(
        '%(levelname)s [%(name)s, %(lineno)d]: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
