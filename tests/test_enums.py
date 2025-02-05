from unittest import TestCase

from src.models.suppliers.enums import SupplierBaseUrl


class TestSupplierBaseUrl(TestCase):
    def test1(self):
        with self.assertRaises(ValueError):
            SupplierBaseUrl("BIKESTER")

    def test2(self):
        assert SupplierBaseUrl["BIKESTER"] == SupplierBaseUrl.BIKESTER
