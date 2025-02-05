import logging
from datetime import datetime, timedelta, timezone
from pprint import pprint
from typing import List

import config
from src.models.marketplaces.sello import Sello
from src.models.marketplaces.sello.order import SelloOrder
from src.views.marketplaces.sello.order import SelloOrderView

logger = logging.getLogger(__name__)


class SelloOrders(Sello):
    number_of_orders_to_fetch: int = config.sello_number_of_orders_to_fetch
    orders: List[SelloOrder] = []
    orders_to_import: List[SelloOrder] = []

    # @staticmethod
    # def __check_reference__(line: SelloOrderRow):
    #     # This is needed because of missing products and references in Sello.
    #     exceptions = [
    #         # byxskydd
    #         "412381639",
    #         # 2xgummiproppar
    #         "413897728",
    #         # sadelrails
    #         "412381988",
    #         # spegel
    #         "412381819",
    #         # diverse cykeldelar
    #         "424097516",
    #         # plathuv over
    #         "407651220",
    #         # reflex bak
    #         "407653686",
    #         # kedja 1sp
    #         "406004830",
    #         # spann framlykta
    #         "417851613",
    #         # vxl 5pack
    #         "409678830",
    #         "412380712",
    #         # sh tryckst kort
    #         "412379686",
    #         # ekerskydd liten
    #         "407650912",
    #         # ringkl svart liten
    #         "407654461",
    #         # ybn rostsk 1sp
    #         "412384497",
    #         # refl framgaf
    #         "412381941",
    #         # vxlv
    #         "406004198",
    #         "409679031",
    #         # bromsv
    #         "407652256",
    #         # sadelsk ms
    #         "412381075",
    #         # vxlregl svart 7v
    #         "407649595",
    #     ]
    #     if line["item_no"] in exceptions:
    #         return True
    #     elif line["reference"] is None or line["reference"] == "":
    #         return False
    #     else:
    #         return True

    def __fetch_orders__(self):
        """We get the latest x orders from Sello"""
        r = self.__call_api__(
            "orders?sort=created_at&sort_direction=desc",
            size=self.number_of_orders_to_fetch,
            offset=0,
        )
        json = r.json()
        self.orders = []
        for order in json["orders"]:
            if config.debug_responses:
                pprint(order)
            if len(order["rows"]) == 0:
                logger.error("this order has no rows")
                # raise ValueError("this order has no rows")
            else:
                # We only import orders with rows
                self.orders.append(SelloOrderView(**order))
        # We get newest first from Sello but we want to import
        # the oldest first in Dolibarr so we reverse the list
        self.orders.reverse()
        logger.info(f"Got {len(self.orders)} orders")

    def __determine_orders_to_import__(self):
        for order in self.orders:
            if order.can_be_imported:
                self.orders_to_import.append(order)
