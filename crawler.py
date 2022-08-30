from datetime import timedelta
import config as conf
import requests
import output
import time
import log
import re


class Crawler:
    def __init__(self) -> None:

        self.__product_list = []
        self.__logger = log.get_logger()
        self.__config = conf.create_config_file()
        self.__sc = ""
        self.__number_of_pages = 0
        self.__index_a = 0
        self.__index_b = 23
        self.__size = 24
        self.__headers = ""

    def start(self) -> None:

        self.__prepare_crawler()
        starting_time = time.time()

        page = 0
        while page < self.__number_of_pages:

            url = "https://www.hiperlibertad.com.ar" \
                  "/api/catalog_system/pub/products/search/api?O=OrderByTopSaleDESC" \
                  f"&_from={self.__index_a}&_to={self.__index_b}&ft&{self.__sc}"

            response = {}

            try:
                attempts = int(self.__config["FILE"]["attempts"])

            except KeyError as e:
                self.__logger.error(f"Error reading config file: {e}")
                attempts = 1

            try_ = 0
            while try_ < attempts:

                try:
                    response = requests.get(url=url, headers=self.__headers).json()
                    self.__logger.info(f"Connect to {url}")
                    print(url)
                    break

                except Exception as e:

                    self.__logger.error(f"Cant get {url} - {e}")

                    # Time to wait per attempt. It could be a configuration option.
                    time.sleep(2.0)
                    try_ += 1

            try:
                for index in range(len(response)):
                    product = {
                        "name": response[index]["productName"],
                        "categories": response[index]["categories"][0],
                        "url": response[index]["link"],
                        "description": response[index]["description"],
                        "list_price": response[index]["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"],
                        "price": response[index]["items"][0]["sellers"][0]["commertialOffer"]["Price"],
                        "sku": re.search(r"sku=\d+",
                                         response[index]["items"][0]["sellers"][0]["addToCartLink"]).group()[4:],
                        "stock": response[index]["items"][0]["sellers"][0]["commertialOffer"]["AvailableQuantity"]
                    }
                    self.__product_list.append(product)

            except TypeError as e:

                self.__logger.info(f"No more products to get: {e}")
                break

            except KeyError as e:

                self.__logger.error(f"Cannot take data. Key: {e} not exist")

            self.__index_a = self.__index_b + 1
            self.__index_b = self.__index_b + self.__size

            page += 1

        self.__save()
        ending_time = time.time()

        self.__logger.info(f"Time elapsed: {timedelta(seconds=ending_time - starting_time)}")

    def __prepare_crawler(self):

        self.__config.read("hiperlibertad/config.ini")

        self.__logger.info("Crawler started...")

        try:
            # Take branch number from url.
            self.__sc = re.search(r"sc=\d+", self.__config["FILE"]["url_web"]).group()
            print(self.__sc)

        except KeyError as e:
            self.__logger.error(f"Error reading config file: {e}")

        try:
            self.__number_of_pages = int(self.__config["FILE"]["number_of_pages"])

        except KeyError as e:
            self.__logger.error(f"Error reading config file: {e}")

        # index_a, index_b, size = Variables used to move between pages
        self.__index_a = 0
        self.__index_b = 23
        self.__size = 24

        self.__headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          "Chrome/104.0.0.0 Safari/537.36",
            "referer": f"https://www.hiperlibertad.com.ar/api?{self.__sc}"
        }

        self.__product_list = []

    def __save(self) -> None:

        count = output.show(self.__product_list)
        output.save_to_csv(self.__product_list)

        self.__logger.info(f"Data products recorded: {count}.")
        self.__logger.info("Crawler finished.")
