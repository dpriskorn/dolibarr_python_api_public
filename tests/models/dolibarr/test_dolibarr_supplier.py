import logging
import unittest

import config
from src.models.dolibarr.enums import Currency
from src.models.dolibarr.supplier import DolibarrSupplier
from src.models.suppliers.enums import SupportedSupplier

logging.basicConfig(level=config.loglevel)

logger = logging.getLogger(__name__)


class DolibarrSupplierTest(unittest.TestCase):
    def setUp(self):
        self.suppliers = []
        print("Checking instantiation of all supported suppliers")
        for s in SupportedSupplier:
            logger.info(f"getting instance of DolibarrSupplier for {s.name}")
            ds = DolibarrSupplier(codename=s)
            ds.update_attributes_from_dolibarr()
            self.suppliers.append(ds)

    def test_supported_suppliers_instances(self):
        for s in self.suppliers:
            self.assertIsInstance(s, DolibarrSupplier)

    def test_supported_suppliers_has_delivery_delay(self):
        for s in self.suppliers:
            self.assertIsNotNone(s.delivery_delay)

    def test_supported_suppliers_has_currency(self):
        for s in self.suppliers:
            self.assertIsInstance(s.currency, Currency)

    # def test_eur_supplier(self):
    #     for s in self.suppliers:
    #         self.assertIsNotNone(s.EUR_supplier)


if __name__ == "__main__":
    unittest.main()
