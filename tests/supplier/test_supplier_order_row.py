import logging
from unittest import TestCase

import config
from src.models.dolibarr.enums import StockType
from src.models.supplier.order_row import SupplierOrderRow
from src.models.suppliers.hoj24.product import Hoj24Product

logging.basicConfig(level=config.loglevel)


class TestSupplierOrderRow(TestCase):
    def test_to_dolibarr_order_line(self):
        sp = Hoj24Product(sku="18-128-123")
        sp.scrape_product()
        sor = SupplierOrderRow(quantity=1, entity=sp)
        dol = sor.to_dolibarr_order_line()
        # print(dol.product.type)
        assert dol.product.type == StockType.STOCKED
        # self.fail()
