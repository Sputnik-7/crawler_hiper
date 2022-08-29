import os
from configparser import ConfigParser


def create_config_file() -> ConfigParser:
    """
    Create the configuration file necessary for the program to work.
    """

    config = ConfigParser()

    folder = "hiperlibertad"
    config_file = "config.ini"
    fol_conf = f"{folder}/{config_file}"

    if not os.path.exists(fol_conf):

        if not os.path.exists(folder):
            os.mkdir(folder)

        # File is created with the first branch by default.
        config["FILE"] = {

            "path_file": "sc1",
            "name_file": "product_list.csv",
            "url_web": "https://www.hiperlibertad.com.ar"
                       "/api/catalog_system/pub/products/search/api?O=OrderByTopSaleDESC&_from=0&_to=23&ft&sc=1",
            "number_of_pages": 3,
            "attempts": 3
        }
        with(open(file=fol_conf, mode="w", encoding="utf-8")) as f:

            config.write(f)

    return config
