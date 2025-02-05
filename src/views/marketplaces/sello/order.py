import logging
from copy import copy

from simple_term_menu import TerminalMenu

from src.controllers.marketplaces.sello.order import SelloOrderContr
from src.models.exceptions import MissingInformationError
from src.views.marketplaces.sello.order_row import SelloOrderRowView
from src.views.my_base_view import MyBaseView

logger = logging.getLogger(__name__)


class SelloOrderView(SelloOrderContr, MyBaseView):
    @staticmethod
    def yes_no_menu_with_default_no(title: str):
        """It outputs the entry index, starting with 0
        In this case 0 for no and 1 for yes"""
        # see https://pypi.org/project/simple-term-menu/
        choices = ["[n] no", "[y] yes"]
        terminal_menu = TerminalMenu(choices, title=title)
        menu_entry_index = terminal_menu.show()
        return menu_entry_index

    def __ask_if_different_products__(self):
        logger.debug("__ask_if_different_products__: running")
        rows = copy(self.row_objects)
        for row in rows:
            if (
                self.yes_no_menu_with_default_no(
                    title=f"Does: '{row.title}' have multiple different products?:"
                )
                == 1
            ):
                # this runs when there is different products
                split_number = self.ask_int(text="How many different?")
                for count in range(1, split_number + 1):
                    new_row: SelloOrderRowView = copy(row)
                    new_row.title = f"{row.title} ({count})"
                    new_price = row.price / split_number
                    print(
                        f"row price: {row.price} split by "
                        f"{split_number} = "
                        f"{round(new_price)} (brutto) "
                        f"{round(new_price/1.25)} (netto)"
                    )
                    new_row.price = new_price
                    self.row_objects.append(new_row)
                self.row_objects.remove(row)
                # pprint(self.model_dump())
                # exit()
            else:
                logger.debug("not different products")

    def import_order(self) -> None:
        """This method check and then imports the thirdparty and order if they are missing
        It returns True if the import was done and False if it has already been imported"""
        logger.debug("import_order: Running")
        if self.is_deleted:
            print("Order is deleted in Sello, skipping")
            return
        if not self.is_delivered:
            print("Order is not marked shipped yet, skipping")
            return
        logger.info("Order can be imported")
        # if not self.all_rows_has_references:
        #     if config.loglevel == logging.DEBUG:
        #         print(self.rows)
        #     raise MissingInformationError(
        #         "Not all lines contains references to Dolibarr product"
        #         + "ids. Import of this order was cancelled."
        #     )
        # else:
        self.__import_thirdparty_if_needed__()
        # Check if the order already exist
        dolibarr_order_id = self.find_sello_order_id_or_false(
            thirdparty_id=self.dolibarr_thirdparty_id
        )
        if dolibarr_order_id:
            logger.info(f"Dolibarr order dolibarr_order_id: {dolibarr_order_id}")
            print("The order already exists")
            self.imported = True
        if dolibarr_order_id is False:
            # print(f"Importing Sello order number: {self.sello_id} with title: {self.order_title}")
            print(f"Importing Sello order number: {self.sello_id}")
            self.__get_order_rows__()
            self.__ask_if_different_products__()
            if not self.dolibarr_thirdparty_id:
                raise MissingInformationError("self.dolibarr_thirdparty_id was None")
            self.__import_to_dolibarr__()
            self.press_enter_to_continue()
