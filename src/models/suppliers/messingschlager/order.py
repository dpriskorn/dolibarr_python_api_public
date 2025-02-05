# DISABLED because the test fails
# import logging
# from typing import Optional, List
#
# from openpyxl import load_workbook  # type: ignore
#
# import config
# from config.enums import FreightProductId
# from src.models.dolibarr.supplier.order import DolibarrSupplierOrder
# from src.models.supplier.entity import SupplierEntity
# from src.models.supplier.order.eu_order import SupplierEuOrder
# from src.models.supplier.service import SupplierService
# from src.models.suppliers.enums import SupplierBaseUrl, SupportedSupplier
# from src.models.suppliers.messingschlager.order_row import MessingschlagerOrderRow
# from src.models.suppliers.messingschlager.product import MessingschlagerProduct
# from src.models.vat_rate import VatRate
#
# logging.basicConfig(level=config.loglevel)
# logger = logging.getLogger(__name__)
#
#
# class MessingschlagerOrder(SupplierEuOrder):
#     """This correspond to the data Shimano exposes for orders"""
#
#     base_url: SupplierBaseUrl = SupplierBaseUrl.MESSINGSCHLAGER
#     codename: SupportedSupplier = SupportedSupplier.MESSINGSCHLAGER
#     # discount_percentage = 1.0
#     dolibarr_supplier_order: Optional[DolibarrSupplierOrder] = None
#     file_path: str
#     credit_days: int = 0
#     invoice_delay: int = 0
#     rows: List[MessingschlagerOrderRow] = []
#
#     # TODO import images into doli also when the REST API supports it.
#
#     def __update_products_and_import_if_missing__(self):
#         [row.entity.update_and_import_if_missing() for row in self.rows]
#
#     def __parse_xlsx_invoice__(self) -> None:
#         wb = load_workbook(filename=self.file_path)
#         # print(wb.get_sheet_names())
#         sheet = wb.active
#         last_row = False
#         p: SupplierEntity
#         for x in range(1, 100):
#             ref = sheet.cell(row=x, column=1).value
#             if ref is not None:
#                 # We don't want the row containing FRACHT or the one after
#                 if ref == "FRACHT":
#                     freight_price = sheet.cell(row=x, column=9).value
#                     service = SupplierService(
#                         dolibarr_product_id=FreightProductId.MESSINGSCHLAGER.value,
#                         eur_cost_price=freight_price,
#                         purchase_vat_rate=VatRate.ZERO,
#                     )
#                     row = MessingschlagerOrderRow(product=service, quantity=1)
#                     self.rows.append(row)
#                     last_row = True
#                 elif ["Artikel", "Rechnungspos"] in ref:
#                     # Skip
#                     continue
#                 if last_row is False:
#                     print(f"Processing ref: {ref}")
#                     quantity = sheet.cell(row=x, column=6).value
#                     eur_row_cost_price = sheet.cell(row=x, column=9).value
#                     calculated_eur_cost_price_per_unit = round(
#                         eur_row_cost_price / quantity, 4
#                     )
#                     # logger.debug
#                     print(
#                         f"calculated_eur_cost_price_per_unit: {calculated_eur_cost_price_per_unit}"
#                     )
#                     # raise DebugExit()
#                     p = MessingschlagerProduct(
#                         ref=ref,
#                         eur_cost_price=calculated_eur_cost_price_per_unit,
#                         purchase_vat_rate=VatRate.ZERO,
#                     )
#                     row = MessingschlagerOrderRow(
#                         product=p,
#                         quantity=quantity,
#                     )
#                     self.rows.append(row)
#                     # if p.sku == 466008:
#                     #     print(row.dict())
#                     #     raise DebugExit()
#                     if config.loglevel == logging.DEBUG:
#                         print(row.dict())
#
#     def parse_and_import_order(self):
#         self.order_date = self.ask_date("Ange orderdatum")
#         self.reference = self.ask_mandatory(text="Ange orderreferens")
#         # nice-to-have check early if the order was already imported
#         self.__parse_xlsx_invoice__()
#         self.__update_products_and_import_if_missing__()
#         # raise NotImplementedError(
#         #     "MS order import has been disabled due to "
#         #     "https://github.com/dpriskorn/dolibarr_python_api/issues/29. "
#         #     "Import it manually."
#         # )
#         self.import_order()
#
#     def import_order(self):
#         """Specific order import function that works for MS"""
#         logger.debug("import_order: Running")
#         self.__prepare_for_import_of_order__()
#         if self.__create_order_and_insert_lines__():
#             print(
#                 "Please go to the order and press 'update prices' "
#                 "before continuing to ensure the prices are right."
#             )
#             self.dolibarr_supplier_order.ask_validate()
#             self.dolibarr_supplier_order.ask_make_order()
#
#     @property
#     def url(self) -> str:
#         return f"{self.base_url.value}{self.id}"
#
#         # def import_as_order(
#         #     lines=None,
#         #     ref=None,
#         #     estimated_order_date=None,
#         #     delivery_date=None,
#         #     invoice_date=None,
#         #     payment_date=None,
#         #     freight_price=None,
#         # ):
#         #     """Call library functions to import the order
#         #     Takes lines like [ {"product_id": "1", "quantity": "1"} ]
#         #     Effect: none
#         #     Side effect: entries in the database
#         #     Call: a bunch of library functions
#         #     """
#         #     if lines is None:
#         #         print("Error. Lines are None")
#         #         exit(1)
#         #     print("Importing order")
#         #     data = insert_supplier_order(
#         #         ref,
#         #         codename,
#         #         order_date=estimated_order_date,
#         #         multicurrency_code="EUR",
#         #         multicurrency_tx=currency_conversion_rate,
#         #     )
#         #     order_id = data["order_id"]
#         #     if debug:
#         #         print(f"debug dolibarr order id {data['order_id']}")
#         #     for line in lines:
#         #         crud.create.insert_supplier_order_line(
#         #             data["order_id"],
#         #             line["product_id"],
#         #             line["quantity"],
#         #             codename,
#         #             supplier_vat_rate=0,
#         #             product_type=0,
#         #         )
#         #     # Add MS freight line
#         #     crud.create.insert_supplier_order_line(
#         #         data["order_id"],
#         #         1376,
#         #         1,
#         #         codename,
#         #         supplier_vat_rate=0,
#         #         product_type=1,
#         #         multicurrency_unitprice=freight_price,
#         #         # calculate the unitprice
#         #         unitprice=round(freight_price / currency_conversion_rate, 2),
#         #     )
#         #     crud.update.update_order_totals(order_id)
#         #     print("Order created: " + f"{SupplierBaseUrl}fourn/commande/card.php?id={order_id}")
#         #     print("Order imported successfully")
#         #     # Validate
#         #     # d.call_action_api("supplierorders",order_id,"validate")
#         #     # dl.update_supplier_order_to_approved_and_made(
#         #     #     order_id,
#         #     #     codename=codename,
#         #     #     delivery_date=delivery_date,
#         #     #     order_date=estimated_order_date,
#         #     # )
#         #     # # Invoicing
#         #     # invoice_id = dl.create_supplier_invoice(
#         #     #     order_id,
#         #     #     invoice_date=invoice_date,
#         #     # )
#         #     # dl.validate_supplier_invoice(invoice_id)
#         #     # # Convert to timestamp
#         #     # date_timestamp = int(datetime.timestamp(payment_date))
#         #     # dl.insert_payment_line_on_supplier_invoice(
#         #     #     invoice_id,
#         #     #     date_timestamp,
#         #     # )
#         #     # print( f"""Order {ref} successfully imported,
#         #     # "accept shipping manually""" )
#         #
#         # def import_missing_product(
#         #     ref,
#         #     price,
#         #     quantity,
#         #     data,
#         # ):
#         #     """Import missing product into Dolibarr
#         #     Effect: none
#         #     Side effect: notification and entry in the database
#         #     """
#         #     # import new product by extracting what we need from JO
#         #     # we want label, price, picture
#         #     print(f"Importing product with ref: {ref}")
#         #     product_id = dl.prepare_and_create_new_product(
#         #         # MS only provides english and german labels, the german one is more
#         #         # detailed
#         #         label_en=data["label_en"],
#         #         label_de=data["label_de"],
#         #         quantity=quantity,
#         #         multicurrency_unitprice=price,
#         #         codename=codename,
#         #         supplier_product_id=ref,
#         #         supplier_product_url=data["product_url"],
#         #         supplier_picture_url=data["picture_url"],
#         #         multicurrency_code="EUR",
#         #         currency_conversion_rate=currency_conversion_rate,
#         #     )
#         #     dl.check_and_scrape(product_id, ref, codename)
#         #     return product_id
#         #
#         # def update_price(
#         #     product_id,
#         #     ref,
#         #     price,
#         #     quantity,
#         # ):
#         #     """Update prices and import missing products
#         #     Effect: none
#         #     Side effect: update prices
#         #     Call: none
#         #     """
#         #     # Update price
#         #     crud.create.insert_purchase_price(
#         #         product_id=product_id,
#         #         supplier_product_id=ref,
#         #         lead_time=8,
#         #         codename=codename,
#         #         multicurrency_code="EUR",
#         #         multicurrency_tx=currency_conversion_rate,
#         #         # Add 5% surplus charge to all products by default because we have no
#         #         # way of knowing which has surplus and which does not.
#         #         multicurrency_unitprice=price * 1.05,
#         #         supplier_id=705,
#         #     )
#         #
#         # def find_dolibarr_product_id(ref):
#         #     """Finds the product id or returns False"""
#         #     # check if the product already exist
#         #     return dl.find_product_id_from_extrafield(
#         #         ref,
#         #         codename,
#         #     )
#         #
#         # raise DebugExit("jihaa")
#         #             product_id = dl.find_product_id_from_extrafield(
#         #                 ref,
#         #                 codename,
#         #             )
#         #             if product_id is None:
#         #                 print("Creating new product")
#         #                 # get the label from MS
#         #                 data = dl.scrape_product_from_ms(ref)
#         #                 product_id = import_missing_product(
#         #                     ref,
#         #                     unitprice,
#         #                     quantity,
#         #                     data,
#         #                 )
#         #             else:
#         #                 print(f"Updating price for {dl.product_url(product_id)}")
#         #                 update_price(
#         #                     product_id,
#         #                     ref,
#         #                     unitprice,
#         #                     quantity,
#         #                 )
#         #             # Append line
#         #             lines.append({"product_id": product_id, "quantity": quantity})
#         # # Get the invoice = order date
#         # date = sheet.cell(row=2, column=4).value
#         # delivery_date = date + timedelta(days=8)
#         # invoice_ref = sheet.cell(row=2, column=2).value.replace("R-", "")
#         # # Check if exists already
#         # exists = dl.check_supplier_order_ref("MS", invoice_ref)
#         # if exists:
#         #     logger.info(
#         #         f"Invoice {invoice_ref} already imported "
#         #         + "as order in Dolibarr, skipping"
#         #     )
#         # else:
#         #     # We don't have it - start importing
#         #     if debug:
#         #         print(lines)
#         #     import_as_order(
#         #         lines=lines,
#         #         ref=invoice_ref,
#         #         estimated_order_date=date,
#         #         delivery_date=delivery_date,
#         #         payment_date=date,
#         #         freight_price=freight_price,
#         #     )
