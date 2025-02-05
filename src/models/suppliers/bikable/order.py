# import logging
# from typing import List
#
# import requests
# from bs4 import BeautifulSoup  # type: ignore
#
# from src.models.exceptions import MissingInformationError
# from src.models.supplier.order import SupplierOrder
# from src.models.suppliers.cykelgear.order_row import CykelgearOrderRow
# from src.models.suppliers.cykelgear.product import CykelgearProduct
# from src.models.suppliers.enums import SupplierBaseUrl, SupportedSupplier
#
#
# class CykelgearOrder(SupplierOrder):
#     """This correspond to the data Cykelgear exposes for orders"""
#
#     base_url: SupplierBaseUrl = SupplierBaseUrl.CYKELGEAR
#     codename: SupportedSupplier = SupportedSupplier.CYKELGEAR
#     freight_price: float = 59.0
#     freight_product_id: int = 1873
#     rows: List[CykelgearOrderRow] = []  # type: ignore # mypy: ignore
#     free_freight: bool = True
#     free_freight_limit_amount: int = 499
#     round_up_on_order_total: bool = True
#     insert_payment: bool = True
#     credit_days: int = 0
#
#     def get_details(self, session: requests.Session = None):
#         """Fetch and parse the details of the order"""
#         logger = logging.getLogger(__name__)
#         if session is None:
#             raise Exception("Session was None")
#         r = session.get(self.url())
#         # with open("/tmp/test.html", "w") as f:
#         #     f.write(r.text)
#         if r.status_code == 200:
#             soup = BeautifulSoup(r.text, features="lxml")
#             table = soup.find("main", {"class": "container-lg"})
#             if table is None:
#                 raise Exception(f"Could not find product list for order {self.id}.")
#             if len(table) > 0:
#                 logger.debug("Got order details")
#                 # Note product ref is not in this table only label, quantity and gross buy_price
#                 # but we look it up in the CykelgearProduct class
#                 self.__parse_order_details__(table)
#                 # logger.info(self)
#         else:
#             raise ValueError(f"Got {r.status_code} from {self.codename}")
#
#     def __parse_order_details__(self, table):
#         """Parse the Cykelgear order details"""
#         logger = logging.getLogger(__name__)
#         # logger.debug(f"table:{table}")
#         # Note product id is not in this table only label, quantity and gross buy_price
#         rows = table.findAll("div", {"class": "row"})
#         # Remove the page header
#         # rows.pop(0)
#         # Remove the table header
#         # rows.pop(0)
#         # Remove the last 3 rows that are junk
#         rows = rows[2:-3]
#         # logger.debug(f"order rows:{len(rows)}")
#         # logger.debug(f"rows:{rows}")
#         if len(rows) == 0:
#             raise ValueError("row was 0, something is wrong")
#         # order_rows = []
#         for row in rows:
#             logger.debug(f"row:{row}")
#             # get label
#             link = row.select_one("a")
#             # print(link)
#             image = row.select_one("img")
#             label = image.get("title").strip()
#             if not label:
#                 print(row)
#                 raise MissingInformationError()
#             product_url = link["href"]
#             logger.debug(f"label:{label}, url:{product_url}")
#             if label is None or product_url is None:
#                 raise ValueError("could not find label")
#             divs = row.select("div")
#             # The divs contain the columns of the table
#             # 0) picture
#             # 1) label
#             # 2) gross buy price
#             # 3) quantity
#             cost_price = self.clean_number_to_float(divs[2].get_text(strip=True)) / 1.25
#             logger.debug(f"cost_price:{cost_price}")
#             quantity = int(divs[3].get_text(strip=True))
#             logger.debug(f"quantity:{quantity}")
#             # raise Exception("Format has changed, update parsing")
#             product = CykelgearProduct(
#                 label=label, url=product_url, cost_price=cost_price
#             )
#             product.update_and_import_if_missing()
#             # if not product.found:
#             #     logger.error(
#             #         f"Not appending {label} with quantity {quantity} and cost price {cost_price} "
#             #         f"because it has expired, please fix the order manually"
#             #     )
#             if product.sku is None:
#                 logger.warning(
#                     f"Not appending {label} with quantity {quantity} and cost price {cost_price} "
#                     f"because ref was None, please fix the order manually"
#                 )
#             else:
#                 self.rows.append(CykelgearOrderRow(quantity=quantity, product=product))
#
#     def url(self):
#         return (
#             f"https://www.cykelgear.se/orderstatus?page=orders_info&orders_id={self.id}"
#         )
