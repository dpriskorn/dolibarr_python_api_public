import logging
from unittest import TestCase

import config

logging.basicConfig(level=config.loglevel)


class TestEntities(TestCase):
    pass
    # disabled because it takes forever
    # def test_get_stocked_and_for_sale_and_out_of_stock_at_supplier(self):
    #     e = Entities()
    #     products = e.get_stocked_and_for_sale_and_out_of_stock_at_supplier()
    #     print(f"{len(products)}")

    # disabled because it takes forever
    # def test_get_stockable_products(self):
    #     e = Entities()
    #     products = e.get_stockable_products()
    #     # print(f"{len(products)}")
    #     for product in products:
    #         self.assertIsInstance(product, DolibarrProduct)
    #         assert product.ref is not None
    #         assert product.id is not None
