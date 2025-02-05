import json
import logging

import requests
from bs4 import BeautifulSoup  # type: ignore
from requests import Response

import config
from src.models.dolibarr.enums import Expired
from src.models.exceptions import (
    MissingInformationError,
)
from src.models.supplier.product.sek_bike_product import SekBikeProduct
from src.models.suppliers.enums import SupplierBaseUrl, SupportedSupplier

logger = logging.getLogger(__name__)


class BikableProduct(SekBikeProduct):
    """
    This emulates a product available from bikable
    We don't log in because there is nothing to gain
    from that with this supplier.

    Note about ref:
    the refs of Cykelgear are mostly numeric but some
    have "-" and letters but no spaces
    """

    # Mandatory
    url: str

    codename: SupportedSupplier = SupportedSupplier.BIKABLE
    base_url: SupplierBaseUrl = SupplierBaseUrl.BIKABLE
    found: bool = False
    lead_time: str = ""
    response: Response | None = None
    sku: str = ""

    class Config:  # dead: disable
        arbitrary_types_allowed = True

    def __login__(self):
        # Not needed
        pass

    def __set_to_expired__(self):
        logger.error(f"Got 404 from {self.url}")
        self.expired = Expired.TRUE
        self.sku = self.generate_expired_ref
        # logger.error(f"Product: {self.label} with unknown cost could not be added")
        # raise ProductExpiredError("product not found")

    def __parse_information_from_product_page__(self):
        """This is a js app where everything is in a data-page attribute and rendered in the browser

        rendering is slow so we just match strings instead :)"""
        soup = BeautifulSoup(self.response.text, features="lxml")
        logger.info("Parsing the page")
        # Find the div element with id 'app'
        div_element = soup.find("div", id="app")
        # Extract the data-page attribute
        data_page = div_element.get("data-page")
        data = json.loads(data_page)
        if config.write_test_data:
            with open("/tmp/test.json", "w") as f:
                f.write(json.dumps(data))
        # pprint(data)
        self.image_url = data["props"]["product"]["image"]
        if not self.image_url:
            logger.error(f"No image found, see {self.url}")
            self.image_url = ""
        self.label = data["props"]["product"]["name"]
        if self.label is None:
            raise MissingInformationError("Label was None")
        self.sku = data["props"]["product"]["id"]
        logger.debug(f"found sku:{self.sku}")
        if self.sku is None:
            raise MissingInformationError(f"No ref found, see {self.url}")
        self.description = data["props"]["product"]["description"]
        if not self.description:
            logger.info("no description found")
        self.list_price = float(data["props"]["product"]["price"]["normalized"])
        self.cost_price = round(float(self.list_price) / 1.25, 2)
        if not self.cost_price:
            raise Exception("Cost price was 0")
        # Availability
        self.available = bool(data["props"]["product"]["in_stock"])
        self.lead_time = data["props"]["product"]["stock_data"]["delivery_time_text"]
        self.scraped = True
        logger.info("Scraping completed succesfully")
        # pprint(self.model_dump())
        # exit()

    def __scrape_product__(self):
        self.__check_url__()
        r = requests.get(self.url, allow_redirects=False)
        if r.status_code == 200:
            self.found = True
            self.response = r
            logger.info("Got product details from Cykelgear")
            if config.write_test_data:
                with open("/tmp/test.html", "w") as f:
                    f.write(r.text)
            self.__parse_information_from_product_page__()
        elif r.status_code == 404:
            self.__set_to_expired__()
        else:
            raise ValueError(f"Got {r.status_code} from {self.codename}")

    def __check_url__(self):
        if not self.url:
            raise ValueError("Url is None, lookup by ref is not supported")
        else:
            if type(self.url) is not str:
                raise ValueError("Url must be a string")
            elif self.base_url.value not in self.url:
                raise ValueError(f"Incorrect domain name on {self.url}")

    def generated_url(self):
        """N/A for this supplier"""
