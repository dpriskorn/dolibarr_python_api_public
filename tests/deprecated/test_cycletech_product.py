# import logging
# from unittest import TestCase
#
# from requests import Session
#
# import config
# from src.models.exceptions import ProductNotFoundError
# from src.models.suppliers.cycletech.product import CycletechProduct
#
# logging.basicConfig(level=config.loglevel)
#
#
# class TestCycletechProduct(TestCase):
#     def test_login(self):
#         cp = CycletechProduct()
#         # with self.assertRaises(NotImplementedError):
#         cp.__login__()
#         assert isinstance(cp.session, Session)
#         # CT returns 302 here if not logged in
#         r = cp.session.get(
#             url="https://en.cycletech.nl/webwinkel/klantgegevens/order-history/",
#             allow_redirects=False,
#         )
#         assert r.status_code == 200
#
#     def test_scrape_product_without_en_label(self):
#         cp = CycletechProduct(ref=7601)
#         # with self.assertRaises(NotImplementedError):
#         assert cp.scraped is False
#         cp.scrape_product()
#         assert cp.ref == "7601"
#         assert (
#             cp.url
#             == "https://en.cycletech.nl/webwinkel/products/details/?artdetail=7601"
#         )
#         assert cp.eur_cost_price == 99.45
#         assert (
#             cp.image_url
#             == "https://en.cycletech.nl/_clientfiles/artikelen/F-TECH/7601.png"
#         )
#         assert cp.scraped is True
#         assert (
#             cp.label_en == "Achterwiel 28 x 1 3/8 Nexus 7 (terugtraprem) - "
#             "Zwarte alu Rodi Freeway velg, zwarte RVS parlé"
#         )
#         # assert cp.label == ""
#
#     def test_scrape_product_with_en_label(self):
#         cp = CycletechProduct(ref=5637)
#         # with self.assertRaises(NotImplementedError):
#         assert cp.scraped is False
#         cp.scrape_product()
#         assert cp.ref == "5637"
#         assert (
#             cp.url
#             == "https://en.cycletech.nl/webwinkel/products/details/?artdetail=5637"
#         )
#         assert cp.eur_cost_price == 86.24
#         assert (
#             cp.image_url
#             == "https://en.cycletech.nl/_clientfiles/artikelen/Foto's%20website%20NINO/5637.jpg"
#         )
#         assert cp.scraped is True
#         assert (
#             cp.label_en
#             == "Shimano SG-C3001-7C Coaster brake Nexus 7 internals 184mm axle."
#         )
#         # assert cp.label == ""
#
#     def test_scrape_product_invalid_number(self):
#         with self.assertRaises(ValueError):
#             cp = CycletechProduct(ref=56372)
#             cp.scrape_product()
#
#     def test_scrape_product_non_existent(self):
#         # https://en.cycletech.nl/webwinkel/products/details/?artdetail=9999
#         with self.assertRaises(ProductNotFoundError):
#             cp = CycletechProduct(ref=9999)
#             cp.scrape_product()
