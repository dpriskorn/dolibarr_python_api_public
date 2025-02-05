import logging

import config
from src.controllers.my_base_contr import MyBaseContr
from src.models.marketplaces.sello.orders import SelloOrders

logger = logging.getLogger(__name__)


class SelloOrdersContr(MyBaseContr, SelloOrders):
    def __process_orders__(self):
        if not self.orders_to_import:
            raise ValueError("self.orders_to_import was empty")
        count_imported = 0
        count_processed = 1
        for order in self.orders_to_import:
            print(
                f"Processing {count_processed}/{len(self.orders_to_import)}: \n{order.name} \n{order.order_title} \n{order.date.date()}"
            )
            if config.debug_responses:
                print(order.model_dump())
                # raise DebugExit()
            # Check if the order is within the timespan we import
            order.import_order()
            if order.imported:
                count_imported += 1
            print("---")
            count_processed += 1
        logger.info(
            f"Processed {count_processed} orders and imported {count_imported} of them"
        )

    def import_orders(self):
        self.__fetch_orders__()
        self.__determine_orders_to_import__()
        self.__process_orders__()
