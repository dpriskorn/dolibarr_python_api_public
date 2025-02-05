import logging
from datetime import datetime, timezone, timedelta
from pprint import pprint
from typing import Any, List

from dateutil.parser import isoparse

import config
from src.models.dolibarr import DolibarrEndpoint
from src.models.dolibarr.customer.order import DolibarrCustomerOrder
from src.models.exceptions import MissingInformationError
from src.models.marketplaces.sello import Sello
from src.models.marketplaces.sello.enums import SelloCountryCode
from src.views.marketplaces.sello.order_row import SelloOrderRowView

logger = logging.getLogger(__name__)


class SelloOrder(Sello):
    created_at: str
    customer_address: str
    customer_address_2: str
    customer_alias: str
    customer_country_code: SelloCountryCode
    customer_first_name: str
    customer_last_name: str
    id: int
    shipping_cost: float
    total: float
    is_deleted: bool
    is_delivered: bool

    # Optional
    rows: List[Any] = []  # typing: SelloOrderRowView
    row_objects: List[SelloOrderRowView] = []
    dolibarr_order_id: int = 0
    dolibarr_thirdparty_id: int = 0
    date_from: datetime = datetime(2022, 1, 1, tzinfo=timezone.utc)
    date_until: datetime = datetime(2020, 7, 20, tzinfo=timezone.utc)
    date_until_enabled: bool = False

    # @property
    # def all_rows_has_references(self):
    #     """Checks if all rows have Dolibarr references"""
    #     if self.rows:
    #         for row in self.rows:
    #             if not row.dolibarr_reference:
    #                 logger.warning(
    #                     f"Row {row.title} is missing a "
    #                     f"dolibarr reference. "
    #                     f"Please fix at http://sello.io"
    #                 )
    #                 return False
    #         # If we have not returned yet, all rows have references
    #         return True
    #     else:
    #         raise MissingInformationError("No rows on order")

    @property
    def alias(self):
        return self.customer_alias

    @property
    def date(self):
        return isoparse(self.created_at)

    @property
    def address(self):
        return f"{self.customer_address} {self.customer_address_2}"

    @property
    def dolibarr_order_url(self):
        dolibarr_order = DolibarrCustomerOrder(id=self.dolibarr_order_id)
        return dolibarr_order.url()

    @property
    def name(self):
        return f"{self.customer_first_name} {self.customer_last_name}".title()

    @property
    def net_shipping_cost(self):
        return round(self.shipping_cost / 1.25, 2)

    @property
    def order_title(self) -> str:
        """Generate an order title for the Dolibarr
        order prefixed by the marketplace"""
        if len(self.rows) > 0:
            # logger.info(f"rows: {len(self.rows)}")
            # pprint(self.rows)
            # We hardcode Tradera here for now
            return "tradera: " + self.rows[0]["title"]
        else:
            raise MissingInformationError("self.rows was None")

    @property
    def order_total(self) -> float:
        return self.total

    @property
    def sello_id(self) -> int:
        return int(self.id)

    @property
    def timestamp(self) -> int:
        """Timestamp as Dolibarr wants it"""
        return int(datetime.timestamp(self.date))

    @property
    def tradera_alias(self):
        return self.customer_alias

    def __get_order_rows__(self) -> None:
        """Get the order lines from Sello"""
        logger.debug("__get_order_rows__: Running")
        r = self.__call_api__("orders/", self.id)
        order = r.json()
        self.row_objects = [SelloOrderRowView(**row) for row in order["rows"]]
        logger.info(f"Got {len(self.rows)} order rows from Sello")

    def find_sello_order_id_or_false(self, thirdparty_id: int):
        if not thirdparty_id:
            raise ValueError("did not get a thirdparty_id")
        r = self.api.call_list_api(
            DolibarrEndpoint.CUSTOMER_ORDER, {"thirdparty_ids": thirdparty_id}
        )
        if r.status_code == 200:
            json = r.json()
            # if config.debug_responses:
            #     pprint(json)
            # Find the right one
            for order in json:
                if config.debug_responses:
                    print("Checking order:")
                    pprint(order)
                sello_id = self.extrafield(order, "sello_id")
                if sello_id and sello_id is not None:
                    if config.debug_responses:
                        logger.debug(f"Sello_id: {sello_id}")
                    try:
                        if int(sello_id) == self.sello_id:
                            # We found a match
                            order_id = order["id"]
                            # logger.debug(order_id)
                            dolibarr_order = DolibarrCustomerOrder(id=order_id)
                            logger.debug("Order found: " + f"{dolibarr_order.url()}")
                            return order_id
                        else:
                            logger.debug(f"{sello_id} did not match {self.sello_id}")
                    except ValueError:
                        logger.debug(
                            f"got value error when trying to convert '{sello_id}' to int"
                        )
                        exit()
            # No match found
            print(f"No match for sello id '{self.sello_id}' found in Dolibarr orders.")
            return False
        elif r.status_code == 404:
            print("No order found for this third party.")
            return False
        else:
            print("Error. Failed to look up order.")
            print(r.text)
            raise Exception()

    @property
    def within_accepted_timespan(self):
        """This is based on date_from and date_until"""
        if self.date < self.date_from:
            print(
                "Order found but skipped because the date"
                + " is from before this script was created."
            )
            return False
        elif self.date > (datetime.now(timezone.utc) - timedelta(hours=24)):
            logger.info("Order was made less than 24 hours ago, skipping.")
            return False
        elif self.date > self.date_until and self.date_until_enabled:
            print("Order excluded because of date_until")
            return False
        else:
            return True

    @property
    def can_be_imported(self):
        """Determines based on delivery status, timespan and deletion"""
        return bool(
            self.is_delivered and self.within_accepted_timespan and not self.is_deleted
        )
