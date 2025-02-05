import logging
from typing import List

import config
from src.models.marketplaces.sello import Sello, SelloProduct


class SelloProducts(Sello):
    products: List[SelloProduct] = []

    @property
    def number_of_products(self):
        """Returns total number of products in Sello"""
        if self.products:
            return len(self.products)

    def fetch_all(self):
        # We have less than 500 products
        for i in range(0, 1):
            # TODO use enum for Sello endpoints
            r = self.__call_api__("products", size=200, offset=i)
            json = r.json()
            if json.get("products"):
                raw_products = json["products"]
                for product in raw_products:
                    if config.loglevel == logging.DEBUG and config.debug_responses:
                        print(product)
                        # exit()
                    sello_product = SelloProduct(**product)
                    # if config.loglevel == logging.DEBUG and "5" in sello_product.private_name:
                    # print(product)
                    # print(sello_product.model_dump())
                    # exit()
                    #     press_enter_to_continue()
                    self.products.append(sello_product)
        logging.info(f"got {len(self.products)} orders from Sello")
