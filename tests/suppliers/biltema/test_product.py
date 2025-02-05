import logging
import unittest

import config
from src.models.suppliers.biltema import BiltemaProduct

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)


class BiltemaProductTests(unittest.TestCase):
    """Tests for the BiltemaProduct class"""

    def test_instantiation_with_ref_and_no_url(self):
        p = BiltemaProduct(sku="1246")
        self.assertEqual(p.sku, "1246")

    def test_instantiation_with_no_arguments(self):
        with self.assertRaises(ValueError):
            p = BiltemaProduct()
            p.scrape_product()

    def test_instantiation_with_empty_url(self):
        with self.assertRaises(ValueError):
            p = BiltemaProduct(url="")
            p.scrape_product()

    def test_instantiation_with_invalid_url(self):
        with self.assertRaises(ValueError):
            p = BiltemaProduct(url=1234)  # type: ignore
            p.scrape_product()

    def test_instantiation_with_wrong_url(self):
        with self.assertRaises(ValueError):
            p = BiltemaProduct(
                url="https://www.bikester.se/shimano-bl-mt200-bromshandtag-vanster-811139_2005940.html"
            )
            p.scrape_product()

    @staticmethod
    def test_stock():
        # todo fix this test
        assert True
        # ref = "27-405"
        # p = BiltemaProduct(ref=ref)
        # assert p.get_stock_in_sundsvall() >= 0
        # # det här däcket är nästan alltid i lager
        # ref = "27-0618"
        # p = BiltemaProduct(ref=ref)
        # assert p.get_stock_in_sundsvall() > 0

    @staticmethod
    def test_instantiation_with_valid_ref():
        ref = "27-405"
        p = BiltemaProduct(sku=ref)
        p.scrape_product()
        # print(p)
        assert p.label == "CYKELKEDJA 8-DEL"
        assert p.description == "För max 8-delad bakre frikrans. 116 länkar."
        assert p.generated_url == "https://www.biltema.se/redirect/article/1/sv/27405"
