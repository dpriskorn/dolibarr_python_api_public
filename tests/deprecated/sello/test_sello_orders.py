# import logging
# from unittest import TestCase
#
# import config
# from src.models.marketplaces.sello.orders import SelloOrders
#
# logging.basicConfig(level=config.loglevel)
#
#
# class TestSelloOrders(TestCase):
#     def test_fetch_orders(self):
#         so = SelloOrders()
#         so.__fetch_orders__()
#         assert so.number_of_orders_to_fetch > len(so.orders)
#
#     # Disabled becase it takes 60s
#     # def test_import_orders(self):
#     #     so = SelloOrders()
#     #     so.import_orders()
#
#     # def test_fetch_products(self):
#     #     s = Sello()
#     #     p = s.fetch_products()
#     #     print(p)
#     #     if not p:
#     #         self.fail()
