import json
import logging
from urllib.parse import quote

from bs4 import BeautifulSoup
from requests import Response

from src.controllers.suppliers.csn.login import CsnLoginContr
from src.helpers.enums import FloatCleanType
from src.models.supplier.product.sek_bike_product import SekBikeProduct
from src.models.suppliers.cycleservicenordic import CycleServiceNordic

logger = logging.getLogger(__name__)


class CycleServiceNordicProduct(SekBikeProduct, CycleServiceNordic):
    # Optional
    sku: str = ""

    def __login__(self):
        if self.session is None:
            self.session = CsnLoginContr().login()

    def __scrape_product__(self):
        if self.url:
            if self.base_url.value not in self.url:
                raise ValueError(f"not a valid cycleservicenordic url: {self.url}")
            self.__login__()
            return self.__scrape_product_url__()
        elif self.sku:
            self.__login__()
            return self.__scrape_product_ref__()
        else:
            raise ValueError("Got neither ref nor url.")

    def __scrape_product_ref__(self) -> None:
        """Don't call this directly"""
        if self.session is None:
            raise ValueError("Please include a session and pass it to this function.")
        if self.sku is None:
            logger.error(f"Error. ref: {self.ref} is invalid")
        url = f"{self.base_url.value}en/product-search/?query={quote(self.sku)}"
        r = self.session.get(url=url)
        if r.status_code == 200:
            with open("/tmp/test.html", "w") as f:
                f.write(r.text)
            soup = BeautifulSoup(r.text, features="html5lib")
            product_list = soup.select_one("#product-list-container")
            if product_list is not None:
                a = product_list.find("a")
                if a is not None and len(a) > 0:
                    logger.debug(a)
                    self.url = self.base_url.value + a["href"][1:]
                    # todo test this
                    logger.info(f"found url: {url}")
                    return self.__scrape_product_url__()
            else:
                raise ValueError(f"No product found, see {url}")
        else:
            raise ValueError(f"Got {r.status_code} from Dolibarr")

    def __extract_label__(self, soup):
        label = soup.select_one(".product-details-title").get_text(strip=True)
        if label is not None:
            self.label = label
        else:
            raise ValueError(f"label was not found, see {self.url}")

    def __extract_ean__(self, soup):
        ean_element = soup.select('small[is="details-ean"] span.uk-text-uppercase')
        if ean_element is None:
            raise ValueError(f"no ean found for this product, see {self.url}")
        if ean_element:
            self.ean = ean_element[0].text
        else:
            raise ValueError(f"label was not found, see {self.url}")

    def __extract_json_ld_data__(self, soup):
        logger.debug("__extract_json_ld_data__: running")
        script_tags = soup.select('script[type="application/ld+json"]')
        logger.debug(f"found {len(script_tags)} scripts")
        # Iterate over each script tag
        for script in script_tags:
            try:
                # Extract the content of the script tag
                json_data = script.string.strip()

                # Load the JSON data
                data = json.loads(json_data)
                # pprint(data)
                # Check if the JSON data contains the "image" key
                if "image" in data:
                    self.image_url = data["image"]
                # Check if the JSON data contains the "offers" and "availability" keys
                if "offers" in data and "availability" in data["offers"]:
                    availability = data["offers"]["availability"]
                    # logger.debug(f"availability: {availability}")
                    if "OutOfStock" in availability:
                        self.available = False
                    elif "InStock" in availability:
                        self.available = True
                    else:
                        raise NotImplementedError(
                            f"not supported availability: {availability}"
                        )
                # else:
                #     logger.debug(f"offers not found in data: {data}")
                # Check if the JSON data contains the "sku" key
                if "sku" in data and data["sku"]:
                    # we only update if it has content
                    self.sku = data["sku"]
                # else:
                #     logger.debug(f"no sku key found in the data: {data}")
            except json.JSONDecodeError:
                # Handle the case where the script content is not valid JSON
                continue

    def __extract_prices__(self, soup):
        # Select the div that contains the cost price
        cost_price_div = soup.select_one(
            "div.product-price .uk-text-bold span.uk-h2.uk-text-bold"
        )
        cost_price = None
        if cost_price_div:
            # Extract the text, remove currency symbol and trim the value
            self.cost_price = float(
                cost_price_div.text.strip().replace("SEK", "").strip()
            )

        # Select the div that contains the list price (MSRP)
        list_price_div = soup.select_one("div.product-price .msrp span")
        list_price = None
        if list_price_div:
            # Extract the text, remove "MSRP", currency symbol, and trim the value
            self.list_price = self.clean_number_to_float(
                value=list_price_div.text.strip().replace("MSRP SEK", "").strip(),
                clean_type=FloatCleanType.AMERICAN,
            )

        return cost_price, list_price

    def __extract_description_table__(self, soup):
        # Select the table with the class that contains the specifications
        table = soup.select_one("table.product-specifications")

        # Initialize a list to store each row as a string
        description_lines = []

        # Check if the table is found
        if table:
            # Iterate over all the rows in the table body
            for row in table.select("tbody tr"):
                # Extract all the cells in the row
                cells = row.find_all("td")
                if (
                    len(cells) == 2
                ):  # Ensure there are exactly two cells (key and value)
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    # Format the row as a string and append it to the list
                    description_lines.append(f"{key}: {value}")

        # Join the list into a single string with line breaks
        self.description = "\n".join(description_lines)

    def __extract_brand__(self, soup):
        # Use CSS selector to find the row with "Brand" label
        brand_row = soup.select_one(
            'table.product-specifications tr:has(td:-soup-contains("Brand"))'
        )
        if brand_row:
            # Extract the second <td> element in the row which contains the brand value
            brand_cell = brand_row.find_all("td")[1]
            self.brand = brand_cell.text.strip()

    def __parse_and_extract_data_from_the_html__(self, response: Response):
        soup = BeautifulSoup(response.text, features="lxml")
        self.__extract_label__(soup)
        self.__extract_ean__(soup)
        self.__extract_prices__(soup)
        self.__extract_json_ld_data__(soup)
        self.__extract_description_table__(soup)
        self.__extract_brand__(soup)
        # # # Work around weird URLs with '"'
        # # product_url = url.replace('"', "%22")
        # # logger.debug(self)

    def __scrape_product_url__(self) -> None:
        if self.url is None:
            raise ValueError("Url was None.")
        if self.session is None:
            raise ValueError("Please include a session and pass it to this function.")
        r = self.session.get(self.url)
        if r.status_code == 200:
            with open("/tmp/test.html", "w") as f:
                f.write(r.text)
            logger.info("Got product page")
            self.__parse_and_extract_data_from_the_html__(response=r)
            # logger.debug(f"URL: {url}")
        else:
            raise ValueError(
                f"Error. Product {self.ref} not found "
                + f"on CSN website via {self.url}. Got {r.status_code}"
            )

    def generated_url(self):
        """N/A"""
