import logging
from unittest import TestCase

import config
from src.models.dolibarr.product import DolibarrProduct
from src.models.dolibarr.supplier.order_line import DolibarrSupplierOrderLine
from src.models.exceptions import MissingInformationError

logging.basicConfig(level=config.loglevel)


class TestDolibarrSupplierOrderLine(TestCase):
    def test_calculate_line_prices_product_missing_purchase_price(self):
        p = DolibarrProduct(
            id=2184
        )  # test product without purchase price or cost price
        p = p.get_by_id()
        p.fetch_purchase_data_and_finish_parsing()
        dsl = DolibarrSupplierOrderLine(product=p, quantity=1)
        with self.assertRaises(MissingInformationError):
            dsl.calculate_purchase_line_prices()

    def test_calculate_line_prices_product_with_purchase_price(self):
        p = DolibarrProduct(id=2185)  # test product with purchase price
        p = p.get_by_id()
        p.fetch_purchase_data_and_finish_parsing()
        dsl = DolibarrSupplierOrderLine(product=p, quantity=1)
        assert dsl.quantity == 1
        dsl.calculate_purchase_line_prices()
        if config.loglevel == logging.DEBUG:
            print(dsl)
        assert dsl.total_ttc == 1.25
        assert dsl.total_tva == 0.25
        assert dsl.total_ht == 1.0
