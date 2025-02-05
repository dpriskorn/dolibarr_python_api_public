# import logging
# import unittest
#
# from pydantic_core import ValidationError
#
# import config
# from src.models.dolibarr.enums import Expired
# from src.models.exceptions import ProductExpiredError
# from src.models.suppliers.cykelgear.product import CykelgearProduct
# from src.models.suppliers.enums import SupportedSupplier
#
# logging.basicConfig(level=config.loglevel)
#
#
# class CykelgearProductTests(unittest.TestCase):
#     """Tests for the CykelgearProduct class"""
#
#     def test_instantiation_with_ref_and_no_url(self):
#         with self.assertRaises(ValueError):
#             CykelgearProduct(ref="1246")  # type: ignore
#
#     def test_instantiation_with_no_arguments(self):
#         with self.assertRaises(ValueError):
#             CykelgearProduct()  # type: ignore
#
#     def test_check_url_with_empty_url(self):
#         cp = CykelgearProduct(url="")
#         with self.assertRaises(ValueError):
#             cp.__check_url__()
#
#     def test_instantiation_with_invalid_url(self):
#         cp = CykelgearProduct(url=1234)  # type: ignore
#         with self.assertRaises(ValidationError):
#             cp.__check_url__()
#
#     def test_instantiation_with_wrong_url(self):
#         cp = CykelgearProduct(
#             url="https://www.bikester.se/shimano-bl-mt200-bromshandtag-vanster-811139_2005940.html"
#         )
#         with self.assertRaises(ValueError):
#             cp.__check_url__()
#
#     def test_instantiation_with_product_not_found(self):
#         p = CykelgearProduct(
#             url="https://www.cykelgear.se/reservdelar/bakvaxel/vaxelora/vaxelora-type-x"
#         )
#         with self.assertRaises(ProductExpiredError):
#             p.__scrape_product__()
#         # self.assertEqual(p.ref, "Geardrop003")
#
#     @staticmethod
#     def test_correct_data():
#         p = CykelgearProduct(
#             url="https://www.cykelgear.se/reservdelar/ekrar-nipplar/1-st-alpina-eker-233-mm-silver-nippel-medfoljer"
#         )
#         p.scrape_product()
#         assert p.cost_price == 5.6
#         assert p.list_price == 7
#         assert p.label == "1 st. Alpina eker 2,33 mm silver, nippel medföljer"
#         assert p.ref == "703302XX-14"
#         assert p.codename == SupportedSupplier.CYKELGEAR
#         assert p.image_url == "https://www.cykelgear.se/images/egeralpina10stk2014.jpg"
#         assert p.expired == Expired.FALSE
#         assert p.scraped is True
#         # We get now stock information fro this particular product
#         assert p.available is None
#
#
# if __name__ == "__main__":
#     unittest.main()
