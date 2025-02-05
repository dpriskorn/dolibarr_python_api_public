import logging
import math
from datetime import datetime
from typing import Optional

import config
from src.controllers.my_base_contr import MyBaseContr
from src.models.dolibarr.enums import (
    DolibarrEndpoint,
    DolibarrEndpointAction,
    DolibarrTable,
)
from src.models.dolibarr.supplier.order import DolibarrSupplierOrder
from src.models.dolibarr.supplier.order_line import DolibarrSupplierOrderLine
from src.models.exceptions import MissingInformationError

logger = logging.getLogger(__name__)


class DolibarrSupplierOrderContr(MyBaseContr, DolibarrSupplierOrder):
    def __add_freight_line__(self):
        logger.debug("Not free freight on this order, adding freight line")
        from src.models.dolibarr.product import DolibarrProduct

        freight_product = DolibarrProduct(
            api=self.api, id=self.supplier_order.freight_product_id
        )
        freight_product = freight_product.get_by_id()
        freight_product.cost_price = self.supplier_order.freight_price
        freight_line = DolibarrSupplierOrderLine(
            product=freight_product, quantity=1, round_up=False
        )
        self.lines.append(freight_line)
        logger.info("Freight line added to DolibarrSupplierOrder")

    def __create_order__(self):
        # Check if exists already
        if not self.ref:
            raise MissingInformationError("self.ref was missing")
        logger.debug("Inserting supplier order")
        self.__insert_supplier_order__()

    def __insert_url_extrafield__(self):

        if self.supplier_order.url:
            self.create.insert_extrafield(
                table=DolibarrTable.SUPPLIER_ORDER,
                dolibarr_id=self.id,
                extrafield="supplier_url",
                value=self.supplier_order.url,
            )
            logger.info("Supplier url was inserted into the extrafield 'supplier_url'")

    def __create_order_and_insert_data__(self):
        """Method that orchestrates the correct insertion
        of the new order and lines into Dolibarr and updates
        the order totals

        Returns true when success and false otherwise"""
        print("Creating new order")
        self.__create_order__()
        if self.id:
            self.__insert_lines__()
            self.__insert_url_extrafield__()
            self.update.update_order_totals(order=self)
            # because of weird recursion error we dont show the order url for Bikester
            if self.supplier_order.scraped:
                print(
                    f"Order created: {self.url}, see {self.supplier_order.url} for the original order at the supplier"
                )
            else:
                print(f"Order created: {self.url}")

    def __insert_lines__(self):
        if not self.id:
            raise MissingInformationError("id was None")
        if not self.lines:
            raise MissingInformationError("self.lines was None")
        if not self.supplier_order:
            raise MissingInformationError("self.supplier_order was None. ")
        # Why do we need a vat rate for the order?
        # if not self.purchase_vat_rate:
        #     raise ValueError("Vat rate of this order was None")
        # Prepare
        print("Inserting lines on the order")

        for line in self.lines:
            self.create.insert_supplier_order_line(line=line, order=self)

    def __insert_supplier_order__(self):
        """Insert supplier order"""
        # TODO Check for duplicates
        # if not self.date:
        #     timestamp = int(datetime.timestamp(datetime.now(tz=self.stockholm_timezone)))
        # else:
        #     # assuming datetime object
        #     # Dolibarr expects an int
        #     timestamp = int(datetime.timestamp(order_date))
        if not self.supplier_order:
            raise ValueError("did not get what we need")
        if not self.supplier_order.dolibarr_supplier:
            self.supplier_order.__get_dolibarr_supplier__()
        if not self.supplier_order.dolibarr_supplier.vat_rate:
            raise MissingInformationError(
                "self.supplier_order.dolibarr_supplier.vat_rate was None"
            )
        # Populate the json
        params = {
            "external_ref": "auto",
            "ref_supplier": self.ref,
            "date": self.order_date.timestamp(),
            # "date_livraison": delivery_date_iso,
            "socid": self.supplier_order.dolibarr_supplier.id,
            "multicurrency_code": self.supplier_order.dolibarr_supplier.currency.value,
            "multicurrency_tx": self.currency_rate,
            # # what do these do?
            # "cond_reglement_id": "1",
            # "cond_reglement_code": "RECEP",
            # # pay via SEB
            # "mode_reglement_id": "2",
            # "mode_reglement_code": "VIR",
            "tva_tx": self.supplier_order.dolibarr_supplier.vat_rate.value,
            "note": "Imported with Python via the REST API",
        }
        r = self.api.call_create_api(
            endpoint=DolibarrEndpoint.SUPPLIER_ORDER, params=params
        )
        if r.status_code == 200:
            if config.debug_responses:
                logger.debug(r.text)
            self.id = self.response_to_int_or_fail(r.text)
            if not self.id:
                raise ValueError("Id was None")
            logger.info(f"Inserted new supplier order: {self.url}")
        else:
            raise ValueError(f"Failed to insert supplier order. Got {r.status_code}")

    def __make_order__(self, order_date: Optional[datetime] = None):
        if not self.delivery_date:
            logger.debug("Asking about delivery date")
            self.ask_delivery_date()
        # We default to date for creation of order
        if order_date:
            self.order_date = order_date
        # TODO support delivery date
        self.update.update_supplier_order_to_approved_and_made(order=self)

    def __validate__(self):
        self.api.call_action_api(
            DolibarrEndpoint.SUPPLIER_ORDER,
            object_id=self.id,
            action=DolibarrEndpointAction.VALIDATE,
        )
        logger.info("Validated")
        self.validated = True

    def prepare_and_create_order_with_lines_and_correct_amounts(self):
        """Convenience method that first prepares and then creates the order"""
        logger.debug("prepare_and_create_order_with_lines_and_correct_amounts: running")
        if not self.__already_imported__():
            self.__prepare_creation_of_new_order__()
            self.__create_order_and_insert_data__()

    def __handle_freight_line__(self):
        """Handle free freight from suppliers like CG"""
        logger.debug("__handle_freight_line__: Running")
        if self.supplier_order.add_freight:
            if len(self.lines) == 0:
                raise ValueError(
                    "self.lines should be populated before this method is called"
                )
            free_freight_applicable = False
            if (
                self.supplier_order.free_freight is True
                and self.supplier_order.free_freight_limit_amount
            ):
                if self.supplier_order.round_up_total_gross_line_price:
                    sum_before_freight: float = (
                        sum(
                            math.ceil(line.product.cost_price * line.quantity)
                            for line in self.lines
                        )
                        * 1.25
                    )
                else:
                    sum_before_freight: float = (
                        sum(
                            line.product.cost_price * line.quantity
                            for line in self.lines
                        )
                        * 1.25
                    )
                if self.supplier_order.round_up_on_order_total:
                    logger.debug("Rounding up order total")
                    sum_before_freight = math.ceil(sum_before_freight)
                logger.info(f"Sum before freight:{sum_before_freight}")
                if sum_before_freight > self.supplier_order.free_freight_limit_amount:
                    logger.debug("Free freight on this order, skipping freight line")
                    free_freight_applicable = True
            if not free_freight_applicable:
                self.__add_freight_line__()

    def __prepare_creation_of_new_order__(self):
        """Prepare method which converts into
        dolibarr order lines and calculates line prices"""
        self.__get_dolibarr_supplier__()
        self.__convert_rows_to_dolibarr_order_lines__()
        self.__handle_freight_line__()
        self.__calculate_line_prices__()

    def __calculate_line_prices__(self) -> None:
        [line.calculate_purchase_line_prices() for line in self.lines]

    def __convert_rows_to_dolibarr_order_lines__(self):
        rows = self.supplier_order.rows
        logger.info("Converting rows to dolibarr order lines")
        # We extend here to avoid overwriting an earlier added freight line
        self.lines.extend([row.to_dolibarr_order_line() for row in rows])
