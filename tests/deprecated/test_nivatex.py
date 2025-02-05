# import logging
# import unittest
#
# from src.models import NivatexProduct
#
# logging.basicConfig(level=config.loglevel)
#
#
# class NivatexProductTests(unittest.TestCase):
#     """Tests for the NivatexProduct class"""
#     logger = logging.getLogger(__name__)
#
#     def test_instantiation_with_ref_and_no_url(self):
#         with self.assertRaises(ValueError):
#             NivatexProduct(ref="1246")
#
#     def test_instantiation_with_no_arguments(self):
#         with self.assertRaises(ValueError):
#             NivatexProduct()
#
#     def test_instantiation_with_empty_url(self):
#         with self.assertRaises(ValueError):
#             NivatexProduct(url="")
#
#     def test_instantiation_with_invalid_url(self):
#         with self.assertRaises(ValueError):
#             NivatexProduct(url=1234)  # type: ignore
#
#     def test_instantiation_with_wrong_url(self):
#         with self.assertRaises(ValueError):
#             NivatexProduct(url="https://www.cykelgear.se/reservdelar/bakvaxel/vaxelora/vaxelora-type-x")
#
#     def test_instantiation_with_valid_url(self):
#         raise Exception("finish this...")
#         # p = NivatexProduct(url="")
#         # self.assertEqual(p.external_ref, "")
#
#
# if __name__ == "__main__":
#     unittest.main()
