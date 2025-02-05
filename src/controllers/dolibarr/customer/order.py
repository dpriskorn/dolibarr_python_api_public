import logging
from datetime import datetime

import config
from src.controllers.my_base_contr import MyBaseContr
from src.models.dolibarr import DolibarrEndpoint
from src.models.dolibarr.customer.order import DolibarrCustomerOrder

logger = logging.getLogger(__name__)


class DolibarrCustomerOrderContr(DolibarrCustomerOrder, MyBaseContr):
    timestamp: int = 0
    mode_reglement_id: str = "7"  # default to Tradera
    mode_reglement_code: str = "VIR"

    def create_customer_order(self):
        """Insert customer order"""
        logger.debug("create_customer_order: running")
        # We convert timestamps to int because dolibarr does not accept float timestamps
        if self.timestamp:
            date = self.timestamp
        else:
            if self.date is None:
                date = int(datetime.now().timestamp())
            else:
                date = int(self.date.timestamp())
        # Populate the json
        json = {
            # "external_ref": "auto",
            "socid": self.thirdparty_id,
            "ref_client": self.customer_order_ref,
            "date": date,
            "multicurrency_code": self.multicurrency_code,
            "multicurrency_tx": self.multicurrency_tx,
            # accept payment via SEB only
            "mode_reglement_id": self.mode_reglement_id,
            "mode_reglement_code": self.mode_reglement_code,
            "tva_tx": "25",
            "note": "Imported via the REST API",
        }
        r = self.api.call_create_api(
            endpoint=DolibarrEndpoint.CUSTOMER_ORDER, params=json
        )
        if r.status_code == 200:
            if config.debug_responses:
                print(r.text)
            result = self.response_to_int_or_fail(r.text)
            logger.debug(result)
            return int(result)
        else:
            raise ValueError(
                f"Failed to insert customer order. Got {r.status_code} and {r.text}"
            )

    def add_line_to_customer_order(
        self,
        order_id: int,
        product_id: int,
        quantity: int,
        multicurrency_subprice: float,
        multicurrency_total_ht: float,
        product_type: int,
        # Keyword arguments
        # cost: float = None,
        multicurrency_code: str = "SEK",
        multicurrency_tx: int = 1,  # currency_conversion_rate
        tva_tx: int = 25,
        # date=None,               # tuple from ask_date()
    ):
        # TODO convert to OOP attributes
        # if config.deprecate_database_methods:
        #     raise DeprecatedMethodError()
        """This method inserts a customer order line using
        the Dolibarr Orders API endpoint"""
        # if not self.api:
        #     raise ValueError("self.api was None")
        # fk_multicurrency = get_fk_multicurrency_or_exit(
        #     multicurrency_code,
        # )
        # Calculate the VAT amount and price incl. VAT
        multicurrency_total_tva = multicurrency_total_ht * (tva_tx / 100)
        multicurrency_total_ttc = multicurrency_total_ht * (1 + tva_tx / 100)
        # Populate the json
        json = {
            "external_ref": "auto",
            "fk_product": product_id,
            "product_type": product_type,  # TODO use the enum instead
            "fk_commande": order_id,
            "qty": quantity,
            # Cost is not needed because we get it from the product in Dolibarr automatically
            # "cost_price": cost,
            "price": multicurrency_total_ttc,
            "subprice": multicurrency_subprice,
            "total_ht": multicurrency_total_ht,
            "total_tva": multicurrency_total_tva,
            "total_ttc": multicurrency_total_ttc,
            "multicurrency_code": multicurrency_code,
            "multicurrency_tx": multicurrency_tx,
            "multicurrency_total_ht": multicurrency_total_ht,
            "multicurrency_total_tva": multicurrency_total_tva,
            "multicurrency_total_ttc": multicurrency_total_ttc,
            "tva_tx": "25",
            "note": "Imported via the REST API",
        }
        r = self.api.create_order_line(
            endpoint=DolibarrEndpoint.CUSTOMER_ORDER, dolibarr_id=order_id, params=json
        )
        if r.status_code == 200:
            if config.debug_responses:
                print(r.text)

            result = self.response_to_int_or_fail(r.text)
            logger.debug(result)
            return result
        else:
            print("Failed to insert customer order.")
            print(r.text)
