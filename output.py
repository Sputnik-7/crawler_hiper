import csv
import os
import config as conf


def show(product_list) -> int:
    """
    It prints on the screen the data of the products obtained and returns the total quantity of the same.
    """

    for product in product_list:
        for data in product:
            print(f"{data}: {product[data]}")
        print()

    count = (len(product_list))
    print(count)

    return count


def save_to_csv(product_list) -> None:
    """
    Save product data to a CSV file.
    """

    product_header = ["name", "categories", "url", "description", "list_price", "price", "sku", "stock"]

    config = conf.create_config_file()
    config.read("hiperlibertad/config.ini")

    path_file = config["FILE"]["path_file"]
    name_file = config["FILE"]["name_file"]
    product_file = f"{path_file}/{name_file}"

    if not os.path.exists(product_file):

        if not os.path.exists(path_file):
            os.mkdir(path_file)

    with open(file=product_file, mode="w", encoding="utf-8") as file:

        writer = csv.DictWriter(file, product_header)
        writer.writeheader()
        writer.writerows(product_list)
