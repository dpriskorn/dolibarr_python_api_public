import logging
from datetime import datetime

from bs4 import BeautifulSoup  # type: ignore

from src.models.dolibarr.supplier import DolibarrSupplier
from src.models.supplier.order import SupplierOrder
from src.models.suppliers.enums import SupportedSupplier

logger = logging.getLogger(__name__)
ds = DolibarrSupplier(id=694, codename=SupportedSupplier.HOJ24)
ds.update_attributes_from_dolibarr()


class Hoj24Order(SupplierOrder):
    """This class handles orders from Hoj24"""

    base_url: str = "https://shop.hoj24.se/orders/"
    codename: SupportedSupplier = SupportedSupplier.HOJ24
    delivery_date: datetime
    discount_percentage: float = 0.0
    dolibarr_supplier: DolibarrSupplier = ds
    free_freight: bool = False
    freight_product_id: int = 1544
    reference: int
    credit_days: int = 30
    invoice_delay: int = 2
    insert_payment: bool = True

    @property
    def url(self) -> str:
        return f"{self.base_url}{self.reference}"

    #
    # def get_details(self):
    #     """Fetch and process the order
    #     Call: process_lines()"""
    #     self.__parse_invoice__(self.__fetch_invoice__())
    #
    # def __fetch_invoice__(self):
    #     logger.debug("Fetching invoice details")
    #     self.__login__()
    #     if not self.session:
    #         raise ValueError("Session was None")
    #     r = self.session.get(self.url)
    #     # with open("/tmp/test.html", "w") as f:
    #     #     f.write(r.text)
    #     if r.status_code == 200:
    #         return r
    #     else:
    #         # Note it returns 500 when not found
    #         raise ValueError(
    #             f"Got {r.status_code}. could not fetch order from {self.url}"
    #         )
    #
    # (config=dict(arbitrary_types_allowed=True))
    # def __parse_invoice__(self, response: Response):
    #     logger.debug("Parsing invoice details")
    #     soup = BeautifulSoup(response.text, features="lxml")
    #     lines_table = soup.select(".itemTable")
    #     if len(lines_table) > 0:
    #         lines_table = soup.select(".itemTable")[0]
    #         # We throw away the return of process lines because we do not
    #         # import Jofrab orders.
    #         # We only import their invoices because the orders are botched.
    #         self.parse_lines(lines_table)
    #     else:
    #         logger.error("Error no order lines found.")
