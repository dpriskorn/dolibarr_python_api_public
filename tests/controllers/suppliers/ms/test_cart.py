# from unittest import TestCase
#
# from src.controllers.suppliers.ms.cart import MsCart
# from src.models.suppliers.messingschlager.product import MessingschlagerProduct
#
#
# class TestMsCart(TestCase):
#     # def test_add_not_found(self):
#     #     c = MsCart()
#     #     assert c.add(MessingschlagerProduct(sku=12969), quantity=1) is False
#
#     def test_add_success(self):
#         c = MsCart()
#         response = c.add(MessingschlagerProduct(sku=558052), quantity=1)
#         assert response.on_stock is True
#         assert response.total_amount >= 7.0
