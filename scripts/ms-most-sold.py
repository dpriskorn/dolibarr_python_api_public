import csv
import logging
import os

import config
from src.models.exceptions import NotFoundError
from src.models.suppliers.messingschlager.product import MsProduct

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)


def process_sku(index: int, sku: int):
    print(f"Processing SKU: {sku} with index: {index}")
    directory = "data/ms/topselling/"
    filename = f"{index}-{sku}.jpg"
    # Check if picture has already been downloaded
    if os.path.exists(os.path.join(directory, filename)):
        print(f"Image {filename} already exists.")
        return
    p = MsProduct(sku=sku)
    # get name and picture url from ms
    try:
        p.scrape_product()
        p.get_image_data(filename=filename)
        # press_enter_to_continue()
    except NotFoundError:
        pass


def main():
    # Path to the CSV file
    csv_file_path = (
        "/home/dpriskorn/src/python/dolibarr_python_api/data/ms-topselling-2024.csv"
    )

    # Open and read the CSV file
    with open(csv_file_path) as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if there is one

        # Process each row in the CSV
        for index, row in enumerate(csv_reader):
            sku = int(row[0])
            process_sku(index=index + 1, sku=sku)


if __name__ == "__main__":
    main()
