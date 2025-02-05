# import logging
# import unittest
#
# import config
# from src.models.suppliers.jofrab.invoice import JofrabInvoice
#
# logging.basicConfig(level=config.loglevel)
#
#
# class JofrabInvoiceTests(unittest.TestCase):
#     """We cannot reliably test the parsing of invoices because they disappear after a month"""
#
#     def test_get_details_for_invalid_invoice_number(self):
#         invoice = JofrabInvoice(id=1234)  # type: ignore
#         with self.assertRaises(ValueError):
#             invoice.get_details()
#
#     def test_get_details_for_valid_invoice_number(self):
#         """We cannot reliably test the parsing of invoices because they disappear after a month"""
#         # invoice = JofrabInvoice(id="4428420")
#         # # with self.assertRaises(ValueError):
#         # invoice.get_details()
#         # print(invoice.dict())
#         # # assert invoice.order_date ==
#
#     # def test_jofrab_order(self):
#     #     jo = Jofrab()
#     #     jo.scrape_orders()
