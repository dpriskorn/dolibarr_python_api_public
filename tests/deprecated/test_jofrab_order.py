# import logging
# import unittest
#
# import config
# from src.models.suppliers.jofrab.order import JofrabOrder
#
# logging.basicConfig(level=config.loglevel)
#
#
# class JofrabOrderTests(unittest.TestCase):
#     """We cannot reliably test the parsing of orders because they disappear after a month"""
#
#     def test_get_details_for_invalid_order_number(self):
#         order = JofrabOrder(id=1234)  # type: ignore
#         with self.assertRaises(ValueError):
#             order.__fetch_invoice__()
