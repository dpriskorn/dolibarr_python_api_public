# import logging
# import unittest
#
# import config
# from src.models.suppliers.jofrab import JofrabProduct
#
# logging.basicConfig(level=config.loglevel)
#
#
# class JofrabProductTests(unittest.TestCase):
#     """Tests for the JofrabProduct class"""
#
#     def test_instantiation_with_ref_and_no_url(self):
#         p = JofrabProduct(ref="1246")
#         self.assertEqual(p.ref, "1246")
#
#     def test_instantiation_with_no_arguments(self):
#         p = JofrabProduct()
#         with self.assertRaises(ValueError):
#             p.scrape_product()
#
#     def test_instantiation_with_empty_url(self):
#         p = JofrabProduct(url="")
#         with self.assertRaises(ValueError):
#             p.scrape_product()
#
#     def test_instantiation_with_invalid_url(self):
#         p = JofrabProduct(url=1234)  # type: ignore
#         with self.assertRaises(ValueError):
#             p.scrape_product()
#
#     def test_instantiation_with_wrong_url(self):
#         p = JofrabProduct(
#             url="https://www.cykelgear.se/reservdelar/bakvaxel/vaxelora/vaxelora-type-x"
#         )
#         with self.assertRaises(ValueError):
#             p.scrape_product()
#
#     def test_instantiation_with_valid_url(self):
#         p = JofrabProduct(
#             url="https://www.jofrab.se/cykel/3.-forbrukning-inkl.-dack-slang/"
#             "02.-slang/slang-27%22---29%22/18-328-621_p18-328-621"
#         )
#         p.scrape_product()
#         self.assertEqual(p.ref, "18-328-621")
#
#     @staticmethod
#     def test_import_product():
#         p = JofrabProduct(
#             url="https://www.jofrab.se/cykel/3.-forbrukning-inkl.-dack-slang/"
#             "02.-slang/slang-27%22---29%22/18-328-621_p18-328-621"
#         )
#         p.scrape_product()
#         p.update_and_import_if_missing()
#
#
# if __name__ == "__main__":
#     unittest.main()
