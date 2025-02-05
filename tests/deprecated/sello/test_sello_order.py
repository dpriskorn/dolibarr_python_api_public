# import logging
# from unittest import TestCase
#
# import config
# from src.models.marketplaces.sello.order import SelloOrder
# from src.models.marketplaces.sello.order_row import SelloOrderRow
#
# logging.basicConfig(level=config.loglevel)
#
#
# class TestSelloOrder(TestCase):
#     data = {
#         "account_id": 41900,
#         "attachments": [],
#         "created_at": "2022-05-22T21:18:20.000Z",
#         "currency": "SEK",
#         "customer_address": "Test address",
#         "customer_address_2": "",
#         "customer_alias": "test",
#         "customer_city": "test city",
#         "customer_country_code": "SE",
#         "customer_email": "test@gmail.com",
#         "customer_first_name": "test",
#         "customer_last_name": "test",
#         "customer_mobile": "+46706816700",
#         "customer_phone": "+46706816700",
#         "customer_state": "",
#         "customer_zip": "11111",
#         "delivered_at": None,
#         "icons": [],
#         "id": 35729805,
#         "integration_id": 46162,
#         "is_active": True,
#         "is_deleted": False,
#         "is_delivered": False,
#         "is_new": True,
#         "is_paid": False,
#         "market": 1,
#         "market_name": "Tradera",
#         "market_reference": "114711767",
#         "metadata": {
#             "BillingAddress1": "Test address",
#             "BillingAddress2": "",
#             "BillingCity": "test city",
#             "BillingCountryCode": "SE",
#             "BillingFirstName": "test",
#             "BillingLastName": "test",
#             "BillingZip": "11111",
#         },
#         "notes": None,
#         "number": 153,
#         "payment": {"tradera": []},
#         "payment_option": "",
#         "reminder_sent": False,
#         "returns": [],
#         "row_count": 1,
#         "rows": [
#             {
#                 "created_at": "2022-05-22T21:18:20.000Z",
#                 "id": 37977455,
#                 "identifier": None,
#                 "identifier_type": None,
#                 "image": "https://images.sello.io/products/eac952b45bb694c2574a992020acb061.jpg",
#                 "integration_id": 46162,
#                 "item_no": "542607821",
#                 "item_type": None,
#                 "market_reference": None,
#                 "price": 29,
#                 "product_id": 42950441,
#                 "purchase_price": 0,
#                 "quantity": 1,
#                 "quantity_returned": 0,
#                 "reference": "596",
#                 "status": "accepted",
#                 "status_reason": None,
#                 "stock_location": "",
#                 "submitter": None,
#                 "tariff": None,
#                 "tax": 25,
#                 "title": "Bromsvajer universal",
#                 "total_vat": 5.8,
#                 "total_weight": 0,
#                 "tradera_order_id": 114711767,
#             }
#         ],
#         "shipping_cost": 22,
#         "shipping_option": "Posten",
#         "shipping_reservation_id": None,
#         "status_id": 2662881,
#         "total": 51,
#         "total_eur": 4.86,
#         "total_vat": 10.2,
#         "total_vat_eur": 0.97,
#         "tracking": [],
#         "updated_at": "2022-05-22T21:18:20.000Z",
#         "weight": 0,
#     }
#
#     def test_sello_order_parse(self):
#         so = SelloOrder(**self.data)
#         assert isinstance(so.rows, list)
#         assert isinstance(so.rows[0], SelloOrderRow)
#
#     def test_sello_order_import(self):
#         pass
#         # so = SelloOrder(**self.data)
#         # so.import_order()
#         # test something via the API
#         # TODO delete latest imported customer order
#
#     def test_fix_date_on_invoice(self):
#         pass
#
#     #     so = SelloOrder(**self.data)
#     #     so.__fix_date_on_invoice__(invoice_id=469)
