import logging
from pprint import pprint
from unittest import TestCase

from pydantic_core import ValidationError

import config
from src.models.dolibarr.enums import Currency
from src.models.suppliers.hoj24.product import Hoj24Product

logging.basicConfig(level=config.loglevel)


class Hoj24ProductTests(TestCase):
    """Tests for the Hoj24Product class"""

    def test_instantiation_with_ref_and_no_url(self):
        p = Hoj24Product(sku="1246")
        self.assertEqual(p.sku, "1246")

    @staticmethod
    def test_instantiation_with_valid_ref():
        p = Hoj24Product(sku="18-802-111")
        p.scrape_product()
        exclude = set("session")
        pprint(p.model_dump(exclude=exclude))
        # self.assertEqual(p.sku, "1246")

    def test_instantiation_with_no_arguments(self):
        with self.assertRaises(ValidationError):
            p = Hoj24Product()
            p.scrape_product()

    def test_instantiation_with_empty_url(self):
        with self.assertRaises(ValueError):
            p = Hoj24Product(url="", sku="")
            p.scrape_product()

    def test_instantiation_with_invalid_url(self):
        with self.assertRaises(ValidationError):
            p = Hoj24Product(url=1234, sku="")  # type: ignore
            p.scrape_product()

    def test_instantiation_with_wrong_url(self):
        p = Hoj24Product(
            url="https://www.cykelgear.se/reservdelar/bakvaxel/vaxelora/vaxelora-type-x",
            sku="",
        )
        with self.assertRaises(ValueError):
            p.scrape_product()

    @staticmethod
    def test_generated_url():
        p = Hoj24Product(sku="18-802-111")
        assert p.generated_url == "https://shop.hoj24.se/product/18-802-111"

    @staticmethod
    def test_currency():
        p = Hoj24Product(sku="18-802-111")
        assert p.currency == Currency.SEK

    # @staticmethod
    # def test_import_product():
    #     p = Hoj24Product(
    #         url="https://www.jofrab.se/cykel/3.-forbrukning-inkl.-dack-slang/"
    #         "02.-slang/slang-27%22---29%22/18-328-621_p18-328-621"
    #     )
    #     p.scrape_product()
    #     p.update_and_import_if_missing()


# if __name__ == "__main__":
#     unittest.main()
