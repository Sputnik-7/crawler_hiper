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

    def start(self) -> None:

        starting_time = time.time()

        config = conf.create_config_file()
        config.read("hiperlibertad/config.ini")

        self.__logger.info("Crawler started...")

        # sc = Branch number
        sc = ""
        try:
            # Take branch number.
            sc = re.search(r"sc=\d+", config["FILE"]["url_web"]).group()
            print(sc)

        except KeyError as e:
            self.__logger.error(f"Error reading config file: {e}")

        number_of_pages = 0
        try:
            number_of_pages = int(config["FILE"]["number_of_pages"])

        except KeyError as e:
            self.__logger.error(f"Error reading config file: {e}")

        # index_a, index_b, size = Variables used to move between pages
        index_a = 0
        index_b = 23
        size = 24

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          "Chrome/104.0.0.0 Safari/537.36",
            "referer": f"https://www.hiperlibertad.com.ar/api?{sc}"
        }

        self.__product_list = []

        # Start iterating through the pages.
        page = 0
        while page < number_of_pages:

            url = "https://www.hiperlibertad.com.ar" \
                  "/api/catalog_system/pub/products/search/api?O=OrderByTopSaleDESC" \
                  f"&_from={index_a}&_to={index_b}&ft&{sc}"

            response = {}

            try:
                attempts = int(config["FILE"]["attempts"])

            except KeyError as e:
                self.__logger.error(f"Error reading config file: {e}")
                attempts = 1

            try_ = 0
            while try_ < attempts:

                try:
                    response = requests.get(url=url, headers=headers).json()
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
                        "sku": re.search(r"sku=\d+", response[index]["items"][0]["sellers"][0]["addToCartLink"]).group()[4:],
                        "stock": response[index]["items"][0]["sellers"][0]["commertialOffer"]["AvailableQuantity"]
                    }
                    self.__product_list.append(product)

            except TypeError as e:

                self.__logger.info(f"No more products to get: {e}")
                break

            except KeyError as e:

                self.__logger.error(f"Cannot take data. Key: {e} not exist")

            index_a = index_b + 1
            index_b = index_b + size

            page += 1

        self.save()
        ending_time = time.time()

        self.__logger.info(f"Time elapsed: {timedelta(seconds=ending_time - starting_time)}")

    def save(self) -> None:

        count = output.show(self.__product_list)
        output.save_to_csv(self.__product_list)

        self.__logger.info(f"Data products recorded: {count}.")
        self.__logger.info("Crawler finished.")
