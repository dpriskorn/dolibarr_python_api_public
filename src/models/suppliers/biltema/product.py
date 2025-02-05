import json
import logging
from pprint import pprint
from typing import Any, Dict, List

from bs4 import BeautifulSoup, SoupStrainer  # type: ignore
from requests import Session

import config
from src.models.exceptions import ParseError

# from src.models.exceptions import ParseError
from src.models.supplier.product.sek_bike_product import SekBikeProduct
from src.models.suppliers.enums import SupportedSupplier

logger = logging.getLogger(__name__)


class BiltemaProduct(SekBikeProduct):
    codename: SupportedSupplier = SupportedSupplier.BILTEMA
    found_match: bool = False
    found_data: bool = False
    base_url: str = "https://www.biltema.se"
    # We don't bother saving sessions for Biltema
    session: Session = Session()
    variation_groups: Any = None

    def __login__(self):
        # Not applicable
        pass

    @property
    def sku_without_dash(self):
        """This is needed for some API calls"""
        return self.sku.replace("-", "")

    def parse_cross_sell(self, data=None):
        return self.parse_variations(variations=data["relatedEntries"])

    def parse_variations(self, variations: List[Dict]):
        # if debug_responses:
        #     logger.debug(f"variations:")
        #     pprint(variations)
        for variation in variations:
            # if debug_responses:
            #     logger.debug("variation:")
            #     pprint(variation)
            # Biltema friendly_ref is the article number with a dash, e.g. 27-045
            friendly_sku = variation["articleNumberFriendlyName"]
            logger.debug(f"Found {friendly_sku}")
            sku_without_dash = variation["articleNumber"]
            if friendly_sku == self.sku or sku_without_dash == self.sku_without_dash:
                logger.info("Found match")
                self.found_match = True
                if config.debug_responses:
                    pprint(variation)
                self.description = variation["description"]
                if self.description is None:
                    logger.info("Did not find description.")
                self.cost_price = float(variation["priceIncVAT"]) / 1.25
                if self.cost_price is None:
                    raise ValueError("Error. Did not find cost price.")
                self.list_price = variation["priceIncVAT"]
                if self.list_price is None:
                    raise ValueError("Error. Did not find list price.")
                self.image_url = variation["imageUrlXLarge"]
                if self.image_url is None:
                    raise ValueError("Error. Did not find image url.")
                self.label = variation["name"]
                if self.label is None:
                    raise ValueError("Error. Did not find label.")
                break
        if self.found_match is False:
            logger.debug("Could not find product information in this variation")
        else:
            logger.info("Found all the product information we want")
            # logger.debug("Returning dict")
            # return dict(
            #     bike_product=True,
            #     codename="BT",
            #     description=description,
            #     cost_price=buy_price,
            #     external_ref=ref,
            #     external_image_url=image_url,
            #     label=label,
            #     list_price=list_price,
            #     purchase_vat_rate=25
            # )

    def parse_variation_groups(self):
        for variation_group in self.variation_groups:
            if config.debug_responses:
                logger.debug("variation_group:")
                pprint(variation_group)
            logger.info(f"Parsing variation group {variation_group['name']}")
            self.parse_variations(variations=variation_group["variations"])
        if self.found_match is False:
            logger.debug("Could not find match in any variation group.")

    def parse_lines(self, lines: List):
        for line in lines:
            line = line.strip()
            if line[:18] == "window.productData":
                logger.info("Found data")
                # Clean away garbage
                line = line[43:]
                line = line[:-1]
                # print(line)
                # exit()
                # Convert to json
                json_data = json.loads(line)
                logger.debug("Dumping json to /tmp/test.json")
                del json_data["otherCustomersAlsoBought"]
                del json_data["upSell"]
                with open("/tmp/test.json", "w") as f:
                    f.write(json.dumps(obj=json_data, indent=4))
                # if config.loglevel == logging.DEBUG:
                #     print(json_data)
                self.variation_groups = json_data["variationGroups"]
                variations = json_data["variations"]
                cross_sell = json_data["crossSell"]
                if len(self.variation_groups) > 0:
                    logger.info(
                        f"Parsing {len(self.variation_groups)} variation groups now"
                    )
                    if config.debug_responses:
                        logger.debug("variation groups:")
                        logger.debug(self.variation_groups)
                    self.parse_variation_groups()
                if len(variations) > 0:
                    logger.info("Parsing variations now")
                    if config.loglevel == logging.DEBUG:
                        print(variations)
                    self.parse_variations(variations=variations)
                if cross_sell and len(cross_sell) > 0:
                    logger.info("Parsing cross sell now")
                    self.parse_cross_sell(data=cross_sell)
                if self.found_match is False:
                    raise ValueError(
                        f"No product data found in variations, variation groups or cross sell. See {self.url}"
                    )

    def __scrape_product__(self):
        logger.debug("scrape_product: running")
        if self.sku or self.url:
            self.scrape_product_url()
        else:
            raise ValueError("Both url and ref was missing.")

    def scrape_product_url(self):
        logger.debug("scrape_product_url: running")
        # Check the URL
        # logger.debug(f"self.url={self.url}")
        # if self.base_url is None:
        #     raise Exception("base_url is missing")
        # logger.debug(f"base_url:{self.base_url}")
        if self.url:
            url = self.url
            if self.base_url not in url:
                raise ValueError(f"Incorrect domain name on {self.url}")
            else:
                logger.info(f"Found biltema URL {self.url}")
        else:
            logger.debug("generating url")
            url = self.generated_url
        # raise Exception("debug exit")
        # if self.sku is None:
        #     logger.debug("scrape_product_url:Got no ref")
        #     self.sku = self.ask_mandatory(text="Ref?")
        # Sometimes the redirect is wrong. E.g. for 27-1848 which is a tire but the redirect is to a bike :/
        logger.debug(f"looking up url:{url}")
        # self.render_page()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            # 'Accept-Encoding': 'gzip, deflate, br',
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }
        r = self.session.get(url=url, headers=headers)
        if r.status_code == 200:
            with open("/tmp/test.html", "w") as f:
                f.write(r.text)
                logger.info("Wrote to file")
            logger.info("Got product page, extracting data")
            soup = BeautifulSoup(r.text, features="lxml")
            scripts = soup.select("script")
            for script in scripts:
                lines = script.text.split("\n")
                if config.loglevel == logging.DEBUG and config.debug_responses:
                    pprint(lines)
                self.parse_lines(lines=lines)
            if self.found_match:
                self.found_data = True
                # Disabled because of 502 error
                # logger.info("Checking stock in Sundsvall")
                # stock_quantity = self.get_stock_in_sundsvall()
                # print(f"Current stock: {stock_quantity}")
                # if stock_quantity:
                #     self.stock_quantity = int(stock_quantity)
                # else:
                #     self.stock_quantity = 0
                # self.restock_date = None
            else:
                raise ValueError("No data found")
            # # Parse HTML content using lxml parser
            # soup = BeautifulSoup(self.html, 'lxml')
            #
            # # Extract JSON content
            # script_content = soup.find("script", attrs={"type": "application/ld+json"})
            # if script_content is None:
            #     raise ValueError("no json-ld data found")
            # print(type(script_content.string))
            # self.data = json.loads(script_content.string)
        else:
            raise ValueError(f"Got {r.status_code} from Biltema. Details: {r.text}")

    # def render_page(self):
    #     from selenium import webdriver
    #     from selenium.webdriver.chrome.service import Service
    #     from selenium.webdriver.common.by import By
    #     from selenium.webdriver.chrome.options import Options
    #     from selenium.webdriver.support import expected_conditions as EC
    #
    #     # Set up options
    #     options = Options()
    #     options.headless = True  # To run Chrome in headless mode
    #
    #     # Set up the Chrome driver service
    #     service = Service('/usr/bin/chromedriver')  # Set the path to your chromedriver executable
    #     service.start()
    #
    #     # Create a new instance of the Chrome driver
    #     driver = webdriver.Chrome(service=service, options=options)
    #
    #     try:
    #         # Navigate to the page you want to render
    #         driver.get(self.url)
    #
    #         # Wait for JavaScript to finish loading
    #         wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
    #         wait.until(EC.presence_of_element_located(
    #             (By.ID, 'productDescription')))  # Wait for the productDescription element
    #
    #         # Once the JavaScript has finished loading, get the HTML content
    #         self.html = driver.page_source
    #
    #         # Save the HTML content to a file
    #         with open('/tmp/test.html', 'w', encoding='utf-8') as f:
    #             f.write(self.html)
    #         print("content saved via selenium")
    #     finally:
    #         # Quit the driver
    #         driver.quit()

    def parse_linked_data(self):
        """The data looks like this:
        {
        "@context": "http://schema.org/",
        "@type": "Product",
        "name": "Cykelkedjor",
        "image": ["https://productimages.biltema.com/v1/Image/product/xlarge/2000018121/1"],
        "description": "",
        "mpn": "27403",
        "brand": {
            "@type": "Brand",
            "name": "Biltema"
            },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "SEK",
            "price": "74.90",
            "priceValidUntil": "2025-04-30",
            "itemCondition": "http://schema.org/NewCondition",
            "seller": {
                "@type": "Organization",
                "name": "Biltema"
                },
            "url": "http://www.biltema.se/cykel-elcykel/cykelreservdelar/cykelkedjor/cykelkedja-2000018121",
            "availability": ""
            }
        }
        """
        if not self.data:
            raise ValueError("No data found on this page")
        # extract offer
        offers = self.data["offer"]
        if len(offers) > 1:
            raise ParseError("found multiple offers which is not supported")
        first_offer = offers[0]
        self.list_price = float(first_offer["price"])
        # todo not working anymore, we get 502
        # logger.info("Checking stock in Sundsvall")
        # stock_quantity = self.check_stock()
        # print(f"Current stock: {stock_quantity}")
        # if stock_quantity:
        #     self.stock_quantity = int(stock_quantity)
        # else:
        #     self.stock_quantity = 0
        self.restock_date = None

    def get_stock_in_sundsvall(self) -> int:
        # Check stock via the biltema API
        # Converted curl to requests format with https://curl.trillworks.com/
        logger.debug("looking up the stock")
        if not self.sku or self.sku is None:
            raise ValueError("ref is missing")
        # import http.client as http_client
        # http_client.HTTPConnection.debuglevel = 1
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://www.biltema.se",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://www.biltema.se/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }
        r = self.session.post(
            url="https://stock.biltema.com/v1/stock/",
            headers=headers,
            # data=ref
            # data='"' +  + '"',
            data=f'"{self.sku_without_dash}"',
        )
        logger.debug(f"stock ref: {self.ref}")
        if r.status_code == 200:
            # with open("/tmp/test.json", "w") as f:
            #     f.write(r.text)
            #     logger.info("Wrote to file")
            logger.info("Got product stock information")
            json_data = r.json()
            # Sundsvall has storeId=135
            for store in json_data:
                if store["storeId"] == 135:
                    # pprint(store)
                    logger.debug("Found Sundsvall among stores")
                    return int(store["quantity"])
            logger.debug("No stock in Sundsvall")
            return 0
        elif r.status_code == 404:
            raise ValueError("Got 404 from Biltema Stock API V1")
        else:
            raise ValueError(f"Got {r.status_code} and body: {r.text}")

    @property
    def generated_url(self) -> str:
        return f"https://www.biltema.se/redirect/article/1/sv/{self.sku_without_dash}"
