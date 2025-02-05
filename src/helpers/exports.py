# # import csv
#
# import config
# from src.helpers.enums import InputType
# # from src.models.dolibarr import DolibarrEndpoint
# from src.models.dolibarr.product import DolibarrProduct
# from src.models.my_dolibarr import MyDolibarr
#
# api = MyDolibarr()
# #
# # EXPORT
# #
#
# # This is used to export an order easily to csv so it can be uploaded to the supplier.
#
#
# def generate_csv(codename):
#     """Generate csv export for supplier order.
#     JO does not support a header
#     MS requires a header
#     """
#     codename = ask_mandatory(
#         input_type=InputType.STRING, text="Codename is needed", unit="str"
#     )
#     order_id = ask_mandatory(
#         input_type=InputType.INTEGER, text="Order id is needed", unit="int"
#     )
#     r = self.api.call_get_api(DolibarrEndpoint.SUPPLIER_ORDER, order_id)
#     header = None
#     if codename == "MS":
#         header = ["Product ID", "Amount", "Your SKU"]
#     if r.status_code == 200:
#         order = r.json()
#         count = 0
#         lines = []
#         if header:
#             lines.append(header)
#         print(len(order["lines"]))
#         for row in order["lines"]:
#             if config.debug_responses:
#                 print(row)
#             order = r.json()
#             product_id = row["fk_product"]
#             r = self.api.call_get_api(DolibarrEndpoint.PRODUCTS, product_id)
#             if r.status_code == 200:
#                 product = DolibarrProduct(**r.json())
#                 product.fetch_purchase_data_and_finish_parsing()
#                 qty = row["qty"]
#                 lines.append([product.external_ref, qty, ""])
#                 count += 1
#             else:
#                 print(r.text)
#
#         my_file = open(f"{codename.lower()}-order-export.csv", "w")
#         with my_file:
#             writer = csv.writer(my_file, delimiter=";")
#             writer.writerows(lines)
#             print("Writing complete")
#
#         print(f"Found {count} lines on order to export")
#     else:
#         print(r.text)
