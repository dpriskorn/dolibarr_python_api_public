import logging
from datetime import datetime
from pprint import pprint

import config
from src.controllers.dolibarr.customer.invoice import DolibarrCustomerInvoiceContr
from src.controllers.dolibarr.customer.order import DolibarrCustomerOrderContr
from src.controllers.my_base_contr import MyBaseContr
from src.controllers.thirdparty import ThirdpartyContr
from src.models.dolibarr import DolibarrEndpoint, DolibarrEndpointAction
from src.models.dolibarr.enums import DolibarrTable
from src.models.marketplaces.sello.order import SelloOrder

logger = logging.getLogger(__name__)


class SelloOrderContr(MyBaseContr, SelloOrder):
    # todo rewrite to only create the order once all the questions has been answered by the user
    imported: bool = False
    # dolibarr_customer_order: DolibarrCustomerOrderContr = None

    def __add_invoice__(self):
        """Add invoice on Dolibarr order"""
        logger.debug("__add_invoice__: running")
        # raise DebugExit()
        r = self.api.call_create_api(
            custom_endpoint="invoices/createfromorder/" + str(self.dolibarr_order_id)
        )
        if r.status_code == 200:
            data = r.json()
            if config.debug_responses:
                print(data)
            invoice_id = data["lines"][0]["fk_facture"]
            # fix the date on the invoice which Dolibarr assumes to be today
            self.__fix_date_on_invoice__(invoice_id=invoice_id)
            logger.debug(f"invoice dolibarr_order_id: {invoice_id}")
            return invoice_id
        else:
            self.__notify__("Could not create invoice")
            raise ValueError(
                f"Could not create invoice. " f"Got {r.status_code} and {r.text}"
            )

    def __add_lines_to_order__(self):
        """Add lines of goods to the Dolibarr order"""
        logger.debug("__add_lines_to_order__: running")
        logger.info(f"Adding {len(self.row_objects)} lines to order")
        for line in self.row_objects:
            # handle special dolibarr items because Dolibarr
            # does not support propagating decreasing stock
            # on virtual products to the underlying products. :/
            # virtual_lot_ids = (
            #     config.virtual_products[item]["virtual_lot_id"]
            #     for item in config.virtual_products
            # )
            # if line.determine_dolibarr_reference in virtual_lot_ids:
            #     product_id = virtual_lot_name = quantity = None
            #     for item in config.virtual_products:
            #         if (
            #             config.virtual_products[item]["virtual_lot_id"]
            #             == line.determine_dolibarr_reference
            #         ):
            #             product_id = config.virtual_products[item]["unit_id"]
            #             quantity = config.virtual_products[item]["quantity"]
            #             virtual_lot_name = item
            #             break
            #     if not product_id or not virtual_lot_name or not quantity:
            #         raise MissingInformationError(
            #             "One of the things we need was missing"
            #         )
            #     logger.info(
            #         f"Inserting a special line with the "
            #         f"virtual product lot {virtual_lot_name} and quantity {quantity}"
            #     )
            #     if config.loglevel == logging.DEBUG:
            #         print(line.dict())
            #     # insert 5 of this product
            #     unitprice = line.multicurrency_subprice / quantity
            #     customer_order = DolibarrCustomerOrderContr()
            #     customer_order.add_line_to_customer_order(
            #         order_id=self.dolibarr_order_id,
            #         product_id=product_id,
            #         quantity=quantity,
            #         # cost=line.gross_price,
            #         multicurrency_subprice=unitprice,
            #         multicurrency_total_ht=line.multicurrency_subprice,
            #         product_type=1,  # stocked product
            #     )
            # else:
            # logger.info("Inserting ordinary line")
            customer_order = DolibarrCustomerOrderContr()
            line.ask_questions()
            if config.loglevel == logging.DEBUG:
                pprint(line.model_dump())
            customer_order.add_line_to_customer_order(
                order_id=self.dolibarr_order_id,
                product_id=line.dolibarr_reference,
                quantity=line.quantity,
                # cost=line.gross_price,
                multicurrency_subprice=line.multicurrency_subprice,
                multicurrency_total_ht=line.multicurrency_subprice * line.quantity,
                product_type=1,  # stocked product
            )

    def __add_payment__(self, invoice_id: int):
        """Add invoice on Dolibarr order"""
        logger.debug("__add_payment__: running")
        # print(
        #     "Assuming order and payment date are the same and that the full"
        #     + "amount was paid."
        # )
        p = {
            "datepaye": self.timestamp,
            "paymentid": config.payment_id,
            "closepaidinvoices": "yes",
            "accountid": config.account_id,
        }
        result = self.api.call_action_api(
            endpoint=DolibarrEndpoint.INVOICES,
            object_id=invoice_id,
            action=DolibarrEndpointAction.PAYMENTS,
            params=p,
        )
        if result.status_code == 200:
            print("Successfully inserted payment on the invoice.")
        else:
            raise ValueError(
                f"Got {result.status_code} and {result.text} from Dolibarr"
            )

    def __add_shipping_line__(self):
        customer_order = DolibarrCustomerOrderContr()
        customer_order.add_line_to_customer_order(
            order_id=self.dolibarr_order_id,
            # we use a generic shipping service http://162.19.226.24/product/card.php?id=1484
            product_id=1484,
            quantity=1,
            multicurrency_subprice=self.net_shipping_cost,
            multicurrency_total_ht=self.net_shipping_cost,
            product_type=0,  # product
        )

    def __create_order__(self) -> int:
        """Creates the order and returns the new dolibarr_order_id of the order"""
        # raise DebugExit()
        logger.debug("__create_order__: running")
        customer_order = DolibarrCustomerOrderContr(
            thirdparty_id=self.dolibarr_thirdparty_id,
            customer_order_ref=self.order_title,
            timestamp=self.timestamp,
        )
        dolibarr_id = customer_order.create_customer_order()
        self.create.insert_extrafield(DolibarrTable.ORDER, dolibarr_id, "sello", 1)
        self.create.insert_extrafield(
            DolibarrTable.ORDER, dolibarr_id, "sello_id", self.sello_id
        )
        return int(dolibarr_id)

    def __import_thirdparty_if_needed__(self):
        """Try finding the thirdparty based on
        tradera_alias and import if not found"""
        logger.debug("__import_thirdparty_if_needed__: running")
        thirdparty = ThirdpartyContr(
            address=self.address,
            given_name=self.customer_first_name,
            family_name=self.customer_last_name,
            tradera_alias=self.tradera_alias,
            country_code=self.customer_country_code,
        )
        thirdparty_id = (
            thirdparty.find_thirdparty_customer_id_by_tradera_alias_or_false()
        )
        logger.debug(f"thirdparty_id:{thirdparty_id}")
        if not thirdparty_id:
            print(f"Importing new customer: {self.name}")
            # input("press enter to continue")
            thirdparty_id = thirdparty.import_thirdparty()
        self.dolibarr_thirdparty_id = int(thirdparty_id)

    def __import_to_dolibarr__(self):
        self.dolibarr_order_id = self.__create_order__()
        self.__add_lines_to_order__()
        self.__add_shipping_line__()
        print(f"Imported order, see {self.dolibarr_order_url}")
        self.press_enter_to_continue()
        self.__validate_order__()
        invoice_id = self.__add_invoice__()
        self.__fix_date_on_invoice__(invoice_id=invoice_id)
        # raise DebugExit()
        self.__validate_invoice__(invoice_id=invoice_id)
        self.__add_payment__(invoice_id=invoice_id)
        # self.__notify__(
        #     f"Ny order: {self.order_title}. \nTotalbelopp: {self.order_total}"
        # )
        self.imported = True

    def __validate_invoice__(self, invoice_id: int):
        """Validate the invoice in Dolibarr"""
        logger.debug("__validate_invoice__: running")
        result = self.api.call_action_api(
            endpoint=DolibarrEndpoint.INVOICES,
            object_id=invoice_id,
            action=DolibarrEndpointAction.VALIDATE,
        )
        if result.status_code == 200:
            print("Successfully validated the invoice.")
        else:
            raise ValueError(f"Got {result.status_code} and {result} from Dolibarr")

    def __validate_order__(self) -> None:
        """Validate the Dolibarr order"""
        logger.debug("Validating order")
        # raise DebugExit()
        self.api.call_action_api(
            endpoint=DolibarrEndpoint.CUSTOMER_ORDER,
            object_id=self.dolibarr_order_id,
            action=DolibarrEndpointAction.VALIDATE,
        )

    def __fix_date_on_invoice__(self, invoice_id):
        """Change the date on the new invoice in Dolibarr to be the order date"""
        invoice = DolibarrCustomerInvoiceContr(
            id=invoice_id,
            # invoice_date=datetime.now(tz=self.stockholm_timezone),
            invoice_date=datetime.fromtimestamp(
                timestamp=self.timestamp, tz=self.stockholm_timezone
            ),
        )
        invoice.update_dates_on_invoice()
