import logging
from datetime import datetime
from typing import Any

from requests import Session

from src.models.supplier.order import SupplierOrder
from src.models.supplier.service import SupplierService
from src.models.suppliers.cycleservicenordic import CycleServiceNordic
from src.models.suppliers.cycleservicenordic.order_row import CycleServiceNordicOrderRow
from src.models.suppliers.cycleservicenordic.product import CycleServiceNordicProduct

logger = logging.getLogger(__name__)


class CycleServiceNordicOrder(SupplierOrder, CycleServiceNordic):
    # Mandatory
    reference: int
    session: Session

    credit_days: int = 30
    invoice_delay: int = 1
    insert_payment: bool = True
    data: Any = None
    found: bool = False

    def populate_order_from_api(self) -> None:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            "Referer": "https://www.cycleservicenordic.com/en/customer-area",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=1",
        }

        r = self.session.get(
            url=self.url,
            headers=headers,
        )
        if r.status_code == 200:
            self.data = r.json()
            if self.data is not None and self.data:
                self.found = True
                # pprint(self.data)
                # exit()
                self.__extract_data__()
            else:
                raise Exception(f"Order details not found for {self.reference} even though we got 200 from CSN")
        else:
            print(f"Order details not found for {self.reference}")

    def __extract_data__(self):
        logger.debug("__extract_data__: running")
        order = self.data["order"]
        self.order_date = datetime.strptime(
            order["orderdate"], "%Y-%m-%dT%H:%M:%S"
        ).astimezone(tz=self.stockholm_timezone)
        logger.debug(f"found order date: {order["orderdate"]}")
        logger.debug(f"self.order_date: {self.order_date}")
        # todo extract rows
        for row in self.data["orderlines"]:
            orderline = row["orderline"]
            if orderline["product"] == "freight":
                if orderline["unitprice"] > 0.0:
                    self.rows.append(
                        SupplierService(
                            label="freight",
                            dolibarr_product_id=1638,  # csn freight service
                            cost_price=orderline["unitprice"],
                        )
                    )
                else:
                    logger.info("Ignoring line with zero freight cost")
            else:
                self.rows.append(
                    CycleServiceNordicOrderRow(
                        entity=CycleServiceNordicProduct(
                            sku=orderline["product"],
                            cost_price=orderline["unitprice"],
                        ),
                        quantity=int(orderline["quantitytodeliver"]),
                    )
                )
        # pprint(self.rows)

    @property
    def url(self) -> str:
        """There is no individual html url available so we return the json one"""
        return f"https://www.cycleservicenordic.com/contextapi/b06086ad-b673-48a7-b1dc-1a5b700655aa/v1/order/archived/877618/{self.reference}"
