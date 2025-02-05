# import logging
#
# from bs4 import BeautifulSoup  # type: ignore
# # from requests import Response
#
# from src.models.suppliers.jofrab import JofrabDocument
#
# logger = logging.getLogger(__name__)
#
#
# class JofrabOrder(JofrabDocument):
#     """This class handles orders from Jofrab"""
#
#     @property
#     def url(self):
#         return (
#             "https://www.jofrab.se/mitt-konto"
#             + f"/order/visaorder?orderNumber={self.id}"
#         )
#
#     def get_details(self):
#         """Fetch and process the order
#         Call: process_lines()"""
#         self.__parse_invoice__(self.__fetch_invoice__())
#
#     def __fetch_invoice__(self):
#         logger.debug("Fetching invoice details")
#         self.__login__()
#         if not self.session:
#             raise ValueError("Session was None")
#         r = self.session.get(self.url)
#         # with open("/tmp/test.html", "w") as f:
#         #     f.write(r.text)
#         if r.status_code == 200:
#             return r
#         else:
#             # Note it returns 500 when not found
#             raise ValueError(
#                 f"Got {r.status_code}. could not fetch order from {self.url}"
#             )
#
#     (config=dict(arbitrary_types_allowed=True))
#     def __parse_invoice__(self, response: Response):
#         logger.debug("Parsing invoice details")
#         soup = BeautifulSoup(response.text, features="lxml")
#         lines_table = soup.select(".itemTable")
#         if len(lines_table) > 0:
#             lines_table = soup.select(".itemTable")[0]
#             # We throw away the return of process lines because we do not
#             # import Jofrab orders.
#             # We only import their invoices because the orders are botched.
#             self.parse_lines(lines_table)
#         else:
#             logger.error("Error no order lines found.")
