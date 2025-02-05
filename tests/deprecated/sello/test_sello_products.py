from unittest import TestCase

from src.models.marketplaces.sello.products import SelloProducts


class TestSelloProducts(TestCase):
    def test_fetch_products(self):
        sp = SelloProducts()
        sp.fetch_all()
        assert sp.number_of_products > 0
