# Disabled because login tests fail
import json
import logging
import os
from datetime import datetime
from io import BytesIO
from typing import Any

import requests
from bs4 import BeautifulSoup  # type: ignore

import config
from src.controllers.suppliers.ms.login import MsLoginContr
from src.helpers.enums import StripType
from src.models.exceptions import MissingInformationError, NotFoundError
from src.models.supplier.product.eu_bike_product import EuBikeProduct
from src.models.suppliers.enums import SupplierBaseUrl, SupportedSupplier
from src.models.vat_rate import VatRate

logger = logging.getLogger(__name__)


class MsProduct(EuBikeProduct):
    """Models a product from Shimano
    We can scrape both from ref and from url.

    SKUs are numeric only so we use int
    """

    # Mandatory
    sku: int

    codename: SupportedSupplier = SupportedSupplier.MESSINGSCHLAGER
    base_url: SupplierBaseUrl = SupplierBaseUrl.MESSINGSCHLAGER
    # MS never informs us about their internal stock so we set it to zero
    external_stock: int = 0
    purchase_vat_rate: VatRate = VatRate.ZERO
    search_url: str = ""
    url: str = ""  # the url we scrape
    json_data: Any = None
    html_data: Any = None

    def __get_json_data__(self):
        r = self.session.get(
            f"{self.base_url.value}m3/ajax/Artikel_filter?q={self.sku}&lang=en&maxResults:1",
        )
        if r.status_code == 200:
            logger.info("Got article json")
            if config.write_test_data:
                with open("/tmp/test.json", "w") as f:
                    f.write(json.dumps(r.json()))
            self.json_data = r.json()
            if config.debug_responses:
                logger.debug(self.json_data)
        else:
            raise ValueError(f"Got {r.status_code} from MS")

    def __parse_json_data__(self):
        numfound = self.json_data.get("Solr").get("response").get("numFound")
        logger.debug(f"{numfound} photos found:")
        if numfound > 0:
            response = self.json_data.get("Solr").get("response")
            # pprint(response)
            # Slice a way the leading "/"
            product_url = response["docs"][0]["url"][1:]
            main_image = response["docs"][0]["hauptbild"]
            self.image_url = (
                f'{self.base_url.value}{main_image[0].replace("300x300/", "")}'
            )
            self.label_de = response["docs"][0]["art_name"].strip()
            # We strip extra spaces and remove double spaces
            self.label_en = response["docs"][0]["name"].strip().replace("  ", " ")
            self.url = f"{self.base_url.value}{product_url}"
        else:
            raise NotFoundError(
                f"Not found in MS Solr, product is probably expired, see {self.search_url}"
            )

    def __get_and_parse_json_data__(self):
        self.__get_json_data__()
        self.__parse_json_data__()

    def __get_html_data__(self):
        if not self.url:
            raise ValueError("self.url was empty")
        logger.debug(f"using URL: {self.url}")
        r = self.session.get(self.url, allow_redirects=False)
        if r.status_code == 200:
            if config.write_test_data:
                with open("/tmp/test.html", "w") as f:
                    f.write(r.text)
            logger.info("Got product page")
            self.html_data = r.text
        elif r.status_code == 301:
            logger.error(
                f"Got redirect, product is probably expired, see {self.search_url}"
            )
        elif r.status_code == 404:
            logger.error(f"Got 404, product is probably expired, see {self.search_url}")
        else:
            raise ValueError(f"Got {r.status_code}")

    def __parse_html_data__(self):
        soup = BeautifulSoup(self.html_data, features="lxml")
        stock_information = soup.select(".stock-info")
        if config.loglevel == logging.DEBUG:
            print(stock_information)
            # raise DebugExit()
        cost_price_div = soup.select(".ms-price-size-huge")
        list_price_div = soup.select("div.row:nth-child(3) > div:nth-child(2)")
        if len(stock_information) > 0:
            stock_information = stock_information[0]
            not_in_stock_restock_date_available = soup.select(".stock-yellow")
            # not_in_stock_restock_date_available = stock_information.find(".stock-yellow")
            in_stock = soup.select(".stock-green")
            not_in_stock = soup.select(".stock-red")
            if config.loglevel == logging.DEBUG:
                print(in_stock)
                print(not_in_stock_restock_date_available)
            if len(not_in_stock_restock_date_available) > 0:
                # "Available from 10-21-2021"
                restock_date_string = stock_information.text.strip()[15:]
                if restock_date_string == "not yet known":
                    restock_date = None
                else:
                    restock_date = datetime.strptime(
                        restock_date_string, "%m-%d-%Y"
                    ).astimezone(tz=self.stockholm_timezone)
                logger.debug(f"restock_date:{restock_date}")
                self.available = False
            elif len(in_stock) > 0:
                self.restock_date = None
                self.available = True
            elif len(not_in_stock) > 0:
                self.restock_date = None
            else:
                logger.debug(stock_information)
                raise ValueError("Could not parse stock information")
        else:
            raise MissingInformationError(
                f"No stock information found :/ see {self.url}"
            )
        if len(cost_price_div) > 0:
            self.eur_cost_price = float(
                self.price_cleanup(StripType.EUR_AFTER, cost_price_div[0].text)
            )
        else:
            raise ValueError(f"Could not find cost price. See {self.url}")
        if len(list_price_div) > 0:
            self.eur_list_price = float(
                self.price_cleanup(StripType.EUR_AFTER, list_price_div[0].text)
            )
        else:
            if int(self.ref) == 460781:
                # These rubber inlays have no list price
                self.eur_list_price = 0.0
            else:
                raise ValueError(
                    f"Could not find list price, see {self.url} and {self.search_url}"
                )

    @staticmethod
    def __get_and_parse_html_data__():
        logger.debug("__get_and_parse_html_data__: running")

    def __scrape_product__(self):
        """We scrape the information we need from the webshop after logging in
        We have to login to get the stock information"""
        logger.debug("__scrape_product__: Running")
        if not self.__valid_sku__():
            raise ValueError(f"SKU: {self.sku} is not a valid MS number")
        if not self.session:
            self.session = MsLoginContr().login()
        self.search_url = f"{self.base_url.value}en/products/_t/?q=" + str(self.sku)
        # https://www.quora.com/Can-beautifulsoup-scrape-
        # javascript-rendered-webpages?share=1
        #  Some of the data we want is in the json only and some in the html
        #  only which is really quite terrible because it forces us to get
        #  multiple resources for each product.
        self.__get_and_parse_json_data__()
        self.__get_and_parse_html_data__()

    def __valid_sku__(self) -> bool:
        """We check that the ref is 6 numbers long"""
        try:
            if self.sku and int(self.sku) and len(str(self.sku)) == 6:
                return True
            else:
                return False
        except TypeError:
            return False

    def generated_url(self):
        raise ValueError(
            "there is no cannonical url based on the ids for MS, use self.url instead."
        )

    def get_image_data(
        self, directory: str = "data/ms/topselling/", filename: str = ""
    ):
        # Download image based on p.image_url
        response = requests.get(self.image_url)
        if response.status_code == 200:
            from PIL import Image

            img = Image.open(BytesIO(response.content))
            # Define the directory and filename
            os.makedirs(directory, exist_ok=True)
            # Save the image to disk
            if not filename:
                filename = f"{self.sku}.jpg"
            img.save(os.path.join(directory, filename))
            print(f"Saved image to {filename}")
        else:
            print(f"Failed to download image for SKU: {self.sku}")
