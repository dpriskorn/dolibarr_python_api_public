# import logging
# import unittest
#
# import config
# from src.models.suppliers.bikester.product import BikesterProduct
#
# logging.basicConfig(level=config.loglevel)
#
#
# class BikesterProductTests(unittest.TestCase):
#     """Tests for the BikesterProduct class"""
#
#     logger = logging.getLogger(__name__)
#
#     def test_instantiation_with_ref_and_no_url(self):
#         with self.assertRaises(ValueError):
#             bp = BikesterProduct(ref="1246")
#             bp.scrape_product()
#
#     def test_instantiation_with_no_arguments(self):
#         with self.assertRaises(ValueError):
#             bp = BikesterProduct()
#             bp.scrape_product()
#
#     def test_instantiation_with_empty_url(self):
#         with self.assertRaises(ValueError):
#             bp = BikesterProduct(url="")
#             bp.scrape_product()
#
#     def test_instantiation_with_invalid_url(self):
#         with self.assertRaises(ValueError):
#             bp = BikesterProduct(url=1234)  # type: ignore
#             bp.scrape_product()
#
#     def test_instantiation_with_wrong_url(self):
#         with self.assertRaises(ValueError):
#             bp = BikesterProduct(
#                 url="https://www.cykelgear.se/reservdelar/bakvaxel/vaxelora/vaxelora-type-x"
#             )
#             bp.scrape_product()
#
#     def test_instantiation_with_valid_url(self):
#         p = BikesterProduct(
#             url="https://www.bikester.se/sv/articles/2.2880.85535/tannus-punkteringskydd-armour-275x26-30-for-slang"
#         )
#         p.scrape_product()
#         self.assertEqual(p.ref, "811139")
#
#
# if __name__ == "__main__":
#     unittest.main()
