# import logging
# from unittest import TestCase
#
# import config
# from src.models.exceptions import FuzzyMatchError, MissingInformationError
# from src.models.suppliers.shimano.pricelist import ShimanoPricelist
#
# logging.basicConfig(level=config.loglevel)
#
#
# class TestShimanoPricelist(TestCase):
#     def test_get_latest_pricelist(self):
#         sp = ShimanoPricelist()
#         sp.__update_to_the_latest_pricelist__()
#
#     def test_load_and_parse_the_pricelist(self):
#         sp = ShimanoPricelist()
#         sp.load_and_parse_the_latest_pricelist()
#
#     def test_get_all_product_item_numbers(self):
#         sp = ShimanoPricelist()
#         with self.assertRaises(MissingInformationError):
#             sp.__get_all_product_item_numbers__()
#
#     def test_get_product_from_pricelist_by_ref(self):
#         sp = ShimanoPricelist()
#         sp.get_valid_product_ref_from_pricelist(ref="11110V0921111TG")
#
#     def test_get_product_from_pricelist_by_ref_not_found_in_myshimano(self):
#         sp = ShimanoPricelist()
#         sp.get_valid_product_ref_from_pricelist(ref="SLC30007L210LA3R")
#
#     def test_get_product_from_pricelist_by_ref_not_found_in_myshimano_and_way_off(self):
#         sp = ShimanoPricelist()
#         with self.assertRaises(FuzzyMatchError):
#             sp.get_valid_product_ref_from_pricelist(ref="SLCäöå")
#
#     def test___get_url_to_latest_pricelist__(self):
#         sp = ShimanoPricelist()
#         sp.__get_url_to_latest_pricelist__()
