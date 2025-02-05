import logging
from datetime import datetime
from typing import Any

import config
from src.controllers.dolibarr.product import DolibarrProductContr
from src.helpers.utilities import vat_rate_to_float_multiplier
from src.models.dolibarr.enums import Expired, Status, StockType
from src.models.exceptions import MissingInformationError
from src.models.supplier.enums import ProductCategory
from src.models.suppliers.enums import BadDataSuppliers, EUR_suppliers
from src.views.my_base_view import MyBaseView

logger = logging.getLogger(__name__)


class DolibarrProductView(MyBaseView, DolibarrProductContr):
    """This class contains all the user facing logic, such as asking for price, etc.

    This class enherits from the controler to keep things simple"""

    def __prepare_before_creating_new_product__(self):
        """We prepare this object based on data from the SupplierProduct
        and ask questions as needed"""
        if not self.supplier_product:
            raise ValueError("self.supplier_product is None")
        self.accountancy_code_buy = self.supplier_product.accountancy_code_buy
        self.accountancy_code_sell = self.supplier_product.accountancy_code_sell
        self.codename = self.supplier_product.codename
        self.cost_price = self.supplier_product.cost_price
        self.expired = Expired.FALSE
        self.external_image_url = self.supplier_product.image_url
        self.external_url = self.supplier_product.url
        self.last_update = datetime.now(tz=self.stockholm_timezone)
        self.purchase_vat_rate = self.supplier_product.purchase_vat_rate
        self.ref = self.supplier_product.generated_dolibarr_ref
        self.sales_vat_rate = self.supplier_product.selling_vat_rate
        self.sku = str(self.supplier_product.sku)
        self.status_buy = Status.ENABLED
        if self.codename in EUR_suppliers:
            self.multicurrency_cost_price = float(self.supplier_product.eur_cost_price)
            if not self.multicurrency_cost_price:
                raise MissingInformationError(
                    f"Cannot import because multicurrency_cost_price "
                    f"was None and it is an EUR supplier, see {self.url}"
                )
            self.__calculate_sek_prices_from_eur__()
        print(f"Importing {self.supplier_product.label}")
        if not self.testing:
            self.__ask_questions__()
        self.__set_default_currency__()

    def __ask_sell__(self):  # pragma: no cover
        if not self.testing:
            if self.ask_yes_no_question("Sell product?"):
                self.set_status_sell(status=Status.ENABLED)
                if self.supplier_product:
                    if self.supplier_product.product_category == ProductCategory.SEWING:
                        logging.debug("Setting accountancy_code_sell=3002")
                        self.accountancy_code_sell = "3002"
                    elif self.supplier_product.product_category == ProductCategory.BIKE:
                        logging.debug("Setting accountancy_code_sell=3001")
                        self.accountancy_code_sell = "3001"
                else:
                    logger.info(
                        "Switch this library to OOP and give DolibarrProduct the SupplierProduct class"
                    )
                    self.accountancy_code_sell = self.ask_int(
                        "Type in the accountancy_code_sell"
                    )
            else:
                logger.debug("Not for sale, type service")
                self.set_status_sell(status=Status.DISABLED)
                self.accountancy_code_sell = "3000"
                # Things not for sale are always a service
                self.type = StockType.SERVICE
                # accountancy_code_buy code is set below

            if self.status_sell == Status.DISABLED and self.type == StockType.SERVICE:
                # Ask for numeric accountancy code
                if self.ask_yes_no_question("Verktyg (kod 5410)?"):
                    self.accountancy_code_buy = "5410"
                else:
                    if self.ask_yes_no_question(
                        "Är det en vara som Dolibarr "
                        + "inte ska hålla koll på? (kod 4010)?"
                    ):
                        self.accountancy_code_buy = "4010"
                    else:
                        if self.ask_yes_no_question(
                            "Är det kläder eller " + "skyddsmaterial? (kod 5480)?"
                        ):
                            self.accountancy_code_buy = "5480"
                        else:
                            print(
                                "Antar att det är en "
                                + "förbrukningsinventarie (kod 5420)"
                            )
                            self.accountancy_code_buy = "5420"

    def __ask_stocked__(self):  # pragma: no cover
        if self.ask_yes_no_question("Stock product?"):
            self.type = StockType.STOCKED
        else:
            self.type = StockType.SERVICE

    def __ask_stock_warning__(self):  # pragma: no cover
        answer = self.ask_int("Stock warning quantity? (Default: 1)")
        if answer:
            self.stock_warning_quantity = answer

    def __ask_stock_desired__(self):  # pragma: no cover
        answer = self.ask_int("Desired stock quantity? (Default: 2)")
        if answer:
            self.stock_warning_quantity = answer

    def __ask_questions__(self):  # pragma: no cover
        logger.debug("__ask_questions__: running")
        logger.debug(f"__ask_questions__: testing: {self.testing}")
        if not self.testing:
            logger.debug("asking questions because testing is false")
            self.__ask_stocked__()
            if (
                self.type == StockType.STOCKED
                and not self.supplier_product.scheduled_for_expiration
            ):
                self.__ask_stock_warning__()
                self.__ask_stock_desired__()
            self.__ask_sell__()
            # We only want multiprices on stuff for sale
            if self.status_sell == Status.ENABLED:
                self.__ask_multiprice__(level=1)
            # if self.sello_status:
            #     if self.sello_status.value == 1:
            #         self.ask_multiprice(level=2)
            #     if not self.postnord:
            #         self.__ask_postnord__()
            #     if not self.schenker:
            #         self.__ask_schenker__()

    def __print_price_difference__(
        self, dolibarr_product: Any
    ) -> None:  # pragma: no cover
        """This informs the user of any price changes"""
        if (
            self.supplier_product
            and self.supplier_product.cost_price
            and dolibarr_product.cost_price
        ) and dolibarr_product.cost_price != self.supplier_product.cost_price:
            if dolibarr_product.cost_price > self.supplier_product.cost_price:
                difference = (
                    dolibarr_product.cost_price - self.supplier_product.cost_price
                )
                print(
                    f"Price lowered with {difference} to {self.supplier_product.cost_price} for {self.label}"
                )
            if dolibarr_product.cost_price < self.supplier_product.cost_price:
                difference = (
                    self.supplier_product.cost_price - dolibarr_product.cost_price
                )
                print(
                    f"Price raised with {difference} to {self.supplier_product.cost_price} for {self.label}"
                )

    def __ask_multiprice__(self, level: int = None):  # pragma: no cover
        """Ask and return net multiprice"""
        # We set higher multiplier for these
        # because their data cannot be imported automatically
        if not self.supplier_product:
            raise MissingInformationError("self.supplier_product was None")
        if not self.supplier_product.codename:
            raise ValueError("self.supplier_product.codename was None")
        level_one_multiplier: float
        level_two_multiplier: float
        if self.supplier_product.codename in [item.value for item in BadDataSuppliers]:
            logger.info("BadDataSupplier detected")
            level_one_multiplier = config.bad_supplier_multiplier_level_one
            level_two_multiplier = config.bad_supplier_multiplier_level_two
        else:
            logger.info("GoodDataSupplier detected")
            level_one_multiplier = config.good_supplier_multiplier_level_one
            level_two_multiplier = config.good_supplier_multiplier_level_two
        if not self.cost_price:
            raise ValueError(
                "cost_price was None. Is this a EU supplier? "
                "Did you add it to EUR_suppliers?"
            )
        if not self.sales_vat_rate:
            raise ValueError("Vat rate was None")
        vat_multiplier = vat_rate_to_float_multiplier(self.sales_vat_rate)
        if level == 1:
            calc = int(self.cost_price * level_one_multiplier)
        elif level == 2:
            calc = int(self.cost_price * level_two_multiplier)
        else:
            raise ValueError(f"level {level} not recognized")
        answer = self.ask_int(
            f"Type in desired price for level {level} "
            + f"[cost={self.cost_price}, default={calc}kr]:"
        )
        if answer == 0 or not answer:
            multiprice1 = calc / vat_multiplier
            logger.debug(f"Setting multiprice{level}: {multiprice1}")
            self.multiprice1 = multiprice1
        else:
            multiprice1 = answer / vat_multiplier
            logger.debug(f"Setting multiprice{level}: {multiprice1}")
            self.multiprice1 = multiprice1

    # def __ask_postnord__(self):
    #     if not self.weight:
    #         raise ValueError("Weight is None")
    #     if self.weight <= 45:
    #         if self.ask_yes_no_question(
    #             "Föreslagen PostNord frakt: 11kr, " + "använd denna?"
    #         ):
    #             self.postnord = Postnord.MAX_50G
    #         else:
    #             self.postnord = Postnord(input("Type in PostNord cost [number]:"))
    #     if 45 < self.weight < 95:
    #         if self.ask_yes_no_question(
    #             "Föreslagen PostNord frakt: 22kr, " + "använd denna?"
    #         ):
    #             self.postnord = Postnord(22)
    #         else:
    #             self.postnord = Postnord(input("Type in PostNord cost [number]:"))
    #     if self.weight >= 95:
    #         print(
    #             "Föreslagen PostNord frakt: 42kr eller 59kr "
    #             + "beroende på om den passar i Blå Påse S"
    #         )
    #         if self.ask_yes_no_question("Passar varan i Blå Påse S?"):
    #             self.postnord = Postnord(42)
    #         elif self.ask_yes_no_question("Passar varan i Blå Påse M?"):
    #             self.postnord = Postnord(59)
    #         else:
    #             self.postnord = Postnord(input("Type in PostNord cost [number]:"))
    #
    # def __ask_schenker__(self):
    #     if self.weight <= 1000:
    #         self.schenker = Schenker(59)
    #         if not self.ask_yes_no_question(
    #             f"Föreslagen Schenker frakt: {self.schenker}kr, " + "använd denna?"
    #         ):
    #             self.schenker = Schenker(input("Type in Schenker cost [number]:"))
    #     if 1000 < self.weight < 2000:
    #         self.schenker = Schenker(67)
    #         if not self.ask_yes_no_question(
    #             f"Föreslagen Schenker frakt: {self.schenker.value}kr, "
    #             + "använd denna?"
    #         ):
    #             self.schenker = Schenker(input("Type in Schenker cost [number]:"))
    #     if 2000 < self.weight < 3000:
    #         self.schenker = Schenker(75)
    #         if not self.ask_yes_no_question(
    #             f"Föreslagen Schenker frakt: {self.schenker.value}kr, "
    #             + "använd denna?"
    #         ):
    #             self.schenker = Schenker(input("Type in Schenker cost [number]:"))

    # def __ask_and_insert_categories__(self):
    #     from src.helpers.crud.create import Create
    #
    #
    #     def ask_user(result):
    #         if result:
    #             print(f"Found {len(result)} results:")
    #             for item in result:
    #                 print(f"{item[1]}: {item[2]}")
    #                 if len(result) == 1:
    #                     ask = self.ask_yes_no_question(
    #                         f"Add product to {result[0][1]}?"
    #                     )
    #                     if ask is True:
    #                         create.insert_product_category(
    #                             result[0][0],
    #                             self.id,
    #                         )
    #                         return True
    #                     else:
    #                         return False
    #
    #     # def search_and_insert_tradera_category():
    #     #     # pseudo code
    #     #     # let user input search term
    #     #     # sql search llx_categories and return cat_id, label
    #     #     # present to user
    #     #     # let user confirm
    #     #     # insert_product_category if y
    #     #     # loop
    #     #     while True:
    #     #         q = input(
    #     #             "Search a tradera category until it only returns "
    #     #             + "one and you get to choose that one:"
    #     #         )
    #     #         if q:
    #     #             # this returns a list of tuples (id,label)
    #     #             try:
    #     #                 int(q)
    #     #                 result = list_tradera_categories(q)
    #     #                 logger.debug(result)
    #     #                 if ask_user(result):
    #     #                     # we found and added a category
    #     #                     break
    #     #                 else:
    #     #                     continue
    #     #             except ValueError:
    #     #                 result = list_tradera_categories("%" + q + "%")
    #     #                 logger.debug(result)
    #     #                 if ask_user(result):
    #     #                     # we found and added a category
    #     #                     break
    #     #                 else:
    #     #                     continue
    #
    #     if not self.sello_status:
    #         raise ValueError("sello_status was None.")
    #     else:
    #         self.__find_root_category__()
    #         # Insert tradera category if stocked product
    #         if self.type == StockType.STOCKED and self.sello_status == Status.ENABLED:
    #             search_and_insert_tradera_category()
