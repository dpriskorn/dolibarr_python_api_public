from unittest import TestCase

from src.models.suppliers.hoj24.order_row import Hoj24OrderRow
from src.models.suppliers.hoj24.product import Hoj24Product


class TestHoj24OrderRow(TestCase):
    def test_hoj24order_row(self):
        p = Hoj24Product(sku="18-567-01", cost_price=10, label="dummy", testing=True)
        # with self.assertRaises(NotImplementedError):
        p.update_and_import_if_missing()
        row = Hoj24OrderRow(entity=p, quantity=1)
        row.to_dolibarr_order_line()
        # assert False
