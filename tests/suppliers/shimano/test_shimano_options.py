# from unittest import TestCase
#
# from pydantic import ValidationError
#
# # from src.models.exceptions import MissingInformationError
# from src.models.suppliers.shimano import ShimanoLogin
# from src.models.suppliers.shimano.product.options import ShimanoProductOptions
# from src.models.suppliers.shimano.product.options_endpoint import (
#     ShimanoProductOptionsEndpoint,
# )
#
#
# class TestShimanoOptions(TestCase):
#     session = ShimanoLogin().login_and_get_session()
#
#     def test_get_no_product_code(self):
#         with self.assertRaises(ValidationError):
#             so = ShimanoProductOptionsEndpoint()  # type: ignore
#             so.get()
#
#     def test_get_gängtapp(self):
#         so = ShimanoProductOptionsEndpoint(
#             product_code="PT101081", session=self.session
#         )
#         option = so.get()
#         assert isinstance(option, ShimanoProductOptions)
#         assert (
#             option.baseOptions_0_selected_name
#             == "Gängtapp TAP-10 10mm till ex. bakväxelöra"
#         )
#         assert option.baseOptions_0_selected_priceData_value == 119.0
#         assert option.brand_name == "Park Tool"
#         assert option.baseProductName == "Gängtapp TAP-10 10mm"
#         assert (
#             option.images_0_url
#             == "https://dassets.shimano.com/content/dam/global/cg1SEHAC/parktool/products/TAP-10_001.jpg"
#         )
#         assert option.leadTime == 2
#         assert option.upc == 763477007650
#
#     def test_get_brake(self):
#         so = ShimanoProductOptionsEndpoint(
#             product_code="EBLMT200RL", session=self.session
#         )
#         option = so.get()
#         assert isinstance(option, ShimanoProductOptions)
#         assert option.baseOptions_0_selected_priceData_value == 60.0
#         # print(option.dict())
#
#     def test_get_fallback(self):
#         if not self.session:
#             raise MissingInformationError()
#         so = ShimanoProductOptionsEndpoint(
#             product_code="Y0BN98020", session=self.session
#         )
#         option = so.get()
#         assert isinstance(option, ShimanoProductOptions)
#         assert option.baseOptions_0_selected_priceData_value == 60.0
#
#     def test_get_fallback_kassett(self):
#         so = ShimanoProductOptionsEndpoint(
#             product_code="ECSHG418130", session=self.session
#         )
#         option = so.get()
#         assert isinstance(option, ShimanoProductOptions)
#         assert option.baseOptions_0_selected_priceData_value == 144.0
