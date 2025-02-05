# from unittest import TestCase
#
# from src.models.exceptions import MissingInformationError
# from src.models.suppliers.shimano import ShimanoLogin
# from src.models.suppliers.shimano.product.endpoint import ShimanoProductEndpoint
# from src.models.suppliers.shimano.product.options import ShimanoProductOptions
#
#
# class TestShimanoProductEndpoint(TestCase):
#     session = ShimanoLogin().login_and_get_session()
#
#     def test_get_brake(self):
#         if not self.session:
#             raise MissingInformationError()
#         so = ShimanoProductEndpoint(product_code="EBLMT200RL", session=self.session)
#         option = so.get()
#         assert isinstance(option, ShimanoProductOptions)
#         assert option.baseOptions_0_selected_priceData_value == 60.0
#         # print(option.dict())
#
#     def test_get_Y0BN98020(self):
#         if not self.session:
#             raise MissingInformationError()
#         so = ShimanoProductEndpoint(
#             product_code="Y0BN98020", session=self.session
#         )
#         option = so.get()
#         assert isinstance(option, ShimanoProductOptions)
#         assert option.baseOptions_0_selected_priceData_value == 60.0
