# import logging
# from typing import List, Optional
#
# import requests
#
# import config
# # from src.models.supplier.order import SupplierOrder
# from src.models.supplier.order_row import SupplierOrderRow
# from src.models.suppliers.enums import SupplierBaseUrl, SupportedSupplier
# from src.models.suppliers.jofrab.document_row import JofrabDocumentRow
# from src.models.suppliers.jofrab.login import JofrabLogin
# from src.models.suppliers.jofrab.product import JofrabProduct
#
#
# class JofrabDocument(SupplierOrder):
#     """This is an abstract class that JofrabOrder
#     and JofrabInvoice inherits from"""
#
#     add_freight = True
#     base_url = SupplierBaseUrl.JOFRAB
#     codename = SupportedSupplier.JOFRAB
#     freight_price = 89.0
#     freight_product_id = 1544
#     rows: List[SupplierOrderRow] = []
#     free_freight = False
#     free_freight_limit_amount: int = 0  # 0 means disabled
#     round_up_on_order_total = False
#     round_up_total_gross_line_price = False
#     scraped = True
#     session: Optional[requests.Session]
#
#     class Config:
#         arbitrary_types_allowed = True
#
#     # try using the init from SupplierOrder
#     # def __init__(self, id: str = None, session: requests.Session = None):
#     #     """Populate the object by scraping from Cykelgear"""
#     #     if not id:
#     #         raise ValueError("Id was None")
#     #     else:
#     #         self.id = id
#     #         self.session = session
#     #         # self.fetch_and_process()
#
#     def __login__(self):
#         jl = JofrabLogin()
#         self.session = jl.get_login_session()
#
#     def parse_lines(self, table):
#         """Process invoice or order lines and populate self.rows"""
#         logger = logging.getLogger(__name__)
#         # lines: List[DolibarrSupplierOrderLine] = []
#         logger.info("Parsing lines")
#         rows = table.findAll("tr")
#         # Remove the header
#         rows.pop(0)
#         # First check if multiple orders are mixed into one invoice
#         # We use a set because sometimes Jofrab prints lines with
#         # the same order number multiple times. Weird.
#         orders = set()
#         for row in rows:
#             tds = row.select("td")
#             for td in tds:
#                 if "Order: " in td.get_text():
#                     orders.add(td)
#         if len(orders) > 1:
#             logger.warning("There are multiple orders on this invoice")
#             self.mixed_invoice = True
#         for row in rows:
#             logger.debug(row)
#             ref = row.select(".articleNumber")
#             # handle ref
#             if len(ref) > 0:
#                 # skip ref=" "
#                 if ref[0].text.strip() == "":
#                     ref = None
#             if ref:
#                 ref = ref[0].text.strip()
#                 logger.debug(f"Found ref: {ref}")
#                 label_td = row.findAll("td")[0]
#                 label = label_td.text.strip()
#                 # remove " kr" from end of price and convert to .-notation
#                 cost_price = row.select(".price")
#                 cost_price = float(
#                     cost_price[0].text.replace(" kr", "").replace(",", ".")
#                 )
#                 quantity = int(row.select(".quantity")[0].text)
#                 if (
#                     label is not None
#                     and cost_price is not None
#                     and quantity is not None
#                 ):
#                     document_row = JofrabDocumentRow(
#                         product=JofrabProduct(
#                             ref=ref,
#                             label=label,
#                             cost_price=cost_price,
#                             session=self.session,
#                         ),
#                         quantity=quantity,
#                     )
#                     if config.loglevel == logging.DEBUG:
#                         logger.debug("Adding the following row")
#                         print(document_row.dict())
#                     self.rows.append(document_row)
#             else:
#                 logger.info("Skipping line with missing ref")
#
#     def fetch_and_process(self):
#         raise Exception("Not ported yet")
