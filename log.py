import os
import logging
from logging import Logger
import config as conf


def get_logger() -> Logger:
    """
    Returns an object logger needed to track program operations.
    """
    config = conf.create_config_file()
    config.read("hiperlibertad/config.ini")

    path_file = config["FILE"]["path_file"]
    name_file = config["FILE"]["name_file"]
    product_file = f"{path_file}/{name_file}"

    if not os.path.exists(product_file):

        if not os.path.exists(path_file):
            os.mkdir(path_file)

    log_format = "%(levelname)s %(asctime)s  - %(message)s"

    logging.basicConfig(filename=f"{path_file}/hiperlibertad_log.log", level=logging.INFO, format=log_format,
                        filemode="w")

    logger = logging.getLogger()

    return logger
