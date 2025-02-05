# import logging
# from datetime import timedelta
#
# import iso8601
# from bs4 import BeautifulSoup  # type: ignore
# # from requests import Response
#
# from src.helpers import utilities
# from src.helpers.enums import StripType
# from src.models.exceptions import MissingInformationError
# from src.models.suppliers.jofrab import JofrabDocument
#
# logger = logging.getLogger(__name__)
#
#
# class JofrabInvoice(JofrabDocument):
#     """This class handles invoices from Jofrab"""
#
#     @property
#     def url(self):
#         return (
#             "https://www.jofrab.se/mitt-konto"
#             + f"/fakturahistorik/visafaktura?invoiceNumber={self.id}"
#         )
#
#     def get_details(self):
#         """Fetch and parse the invoice"""
#         logger.info(f"Getting details for invoice {self.id}")
#         self.__parse_invoice__(response=self.__fetch_invoice__())
#
#     def __fetch_invoice__(self):
#         self.__login__()
#         if not self.session:
#             raise ValueError("self.session was None")
#         logger.info(f"Fetching invoice {self.id}")
#         r = self.session.get(self.url)
#         # with open("/tmp/test.html", "w") as f:
#         #     f.write(r.text)
#         if r.status_code == 200:
#             return r
#         else:
#             logger.error(r.status_code)
#             logger.error("Error could not fetch invoice")
#
#     (config=dict(arbitrary_types_allowed=True))
#     def __parse_invoice__(self, response: Response):
#         soup = BeautifulSoup(response.text, features="lxml")
#         div = soup.select(".leftColumn")
#         # if debug:
#         #     print(div)
#         # Extract what we need
#         div_text = div[0].text
#         div_list = div_text.replace("\t", "").split("\n")
#         # print(div_list)
#         invoice_date_line = div_list[2]
#         invoice_date_text = invoice_date_line.replace("Fakturadatum:  ", "")
#         # Convert to UTC and add 2 hours to stay on the right date
#         self.invoice_date = iso8601.parse_date(invoice_date_text)
#         logger.debug(f"Invoice date: {self.invoice_date}")
#         payment_date_line = div_list[3]
#         payment_date_text = payment_date_line.replace("Förfallodatum:  ", "")
#         # Convert to UTC and add 2 hours to stay on the right date
#         self.payment_date = iso8601.parse_date(payment_date_text)
#         logger.debug(f"Payment date: {self.payment_date}")
#         freight_price_line = div_list[12]
#         self.freight_price = float(
#             utilities.price_cleanup(
#                 StripType.KR_AFTER,
#                 freight_price_line.replace("Fraktpris: ", ""),
#             )
#         )
#         logger.info(f"freight_price found: {self.freight_price} kr")
#         lines_table = soup.select_one(".itemTable")
#         if len(lines_table) > 0:
#             # Get delivery date and estimate order date from the table
#             for tr in lines_table.findAll("tr"):
#                 # if debug: print(tr)
#                 # Skip header
#                 if len(tr.findAll("th")) == 0:
#                     # We are now on the first row
#                     order_line = tr.findAll("td")[0].text
#                     delivery_date_text = order_line.split(" ")[3]
#                     self.delivery_date = iso8601.parse_date("20" + delivery_date_text)
#                     if self.delivery_date:
#                         self.estimated_order_date = self.delivery_date - timedelta(
#                             days=3
#                         )
#                     else:
#                         MissingInformationError("self.delivery_date was None")
#                     logger.debug(f"delivery_date found {self.delivery_date}")
#                     break
#             # We got all we need
#             self.parse_lines(lines_table)
#         else:
#             logger.error("Error no invoice lines found.")
