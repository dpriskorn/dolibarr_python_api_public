from datetime import datetime, timezone
from unittest import TestCase

from src.models.dolibarr.supplier.order import DolibarrSupplierOrder
from src.models.suppliers.hoj24.order import Hoj24Order


class TestDolibarrSupplierOrder(TestCase):
    def test__check_if_already_imported__(self):
        so = Hoj24Order(
            order_date=datetime.now(timezone.utc),
            delivery_date=datetime.now(timezone.utc),
            reference=4653290,
        )
        do = DolibarrSupplierOrder(supplier_order=so)
        assert do.__already_imported__() is True

    def test__check_extrafield__(self):
        dso = DolibarrSupplierOrder(id=537, supplier_order=None)
        dso = dso.get_by_id()
        assert dso.array_options is not None
        assert dso.supplier_url == "https://shop.hoj24.se/orders/4655665"

    def test_has_linked_invoice_true(self):
        dso = DolibarrSupplierOrder(id=537, supplier_order=None)
        dso = dso.get_by_id()
        assert dso.has_linked_invoice is True

    def test_has_linked_invoice_false(self):
        dso = DolibarrSupplierOrder(id=575, supplier_order=None)
        dso = dso.get_by_id()
        assert dso.has_linked_invoice is False
