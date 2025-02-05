import logging
from datetime import datetime, timedelta
from typing import Union

from src.controllers.dolibarr.supplier.order import DolibarrSupplierOrderContr
from src.views.my_base_view import MyBaseView

logger = logging.getLogger(__name__)


class DolibarrSupplierOrderView(MyBaseView, DolibarrSupplierOrderContr):
    def ask_delivery_date(self):
        if not self.supplier_order.dolibarr_supplier.codename:
            raise ValueError("Codename was None")
        else:
            logger.debug("Getting delivery delay from supplier")
            delivery_delay = self.supplier_order.dolibarr_supplier.delivery_delay
            if not delivery_delay:
                raise ValueError(
                    f"Delivery delay for {self.supplier_order.dolibarr_supplier.codename} "
                    f"is None, please fix {self.supplier_order.dolibarr_supplier.url()}"
                )
            # http://www.pressthered.com/adding_dates_and_times_in_python/
            # Add delay to get the delivery date
            delivery_date_datetime = self.order_date + timedelta(days=delivery_delay)
            # https://www.programiz.com/
            # python-programming/datetime/strftime
            delivery_date_iso = delivery_date_datetime.strftime("%Y-%m-%d")
            # answer = False
            answer = self.ask_yes_no_question(
                "Use this suggested delivery date: "
                + f" {delivery_date_iso}? (its based on "
                + "a delivery delay of "
                + f"{delivery_delay} days)",
            )
            if answer:
                logger.debug("User choose the suggested delivery date")
                self.delivery_date = delivery_date_datetime
            elif answer is False:
                self.delivery_date = self.ask_date("Need a delivery date.")
                delivery_date_iso = delivery_date_datetime.strftime("%Y-%m-%d")
                logger.debug("debug: delivery_date_iso: " + f"{delivery_date_iso}")

    def ask_order_date(self) -> Union[datetime, None]:
        answer = input(
            "Type in order date [ddmmyy, default=date of creation of order]:"
        )
        if not answer:
            date = None
        else:
            if len(answer) == 4:
                # Default to current year
                answer = answer + datetime.now(tz=self.stockholm_timezone).strftime(
                    "%y"
                )
            date = datetime.strptime(answer, "%d%m%y").astimezone(
                tz=self.stockholm_timezone
            )
        # https://stackabuse.com/converting-strings-to-datetime-in-python/
        # https://www.programiz.com/python-programming/datetime/strftime
        return date

    def ask_make_order(self):
        if self.id:
            answer = self.ask_yes_no_question("Make order")
            if answer is True:
                order_date = self.ask_order_date()
                self.__make_order__(order_date=order_date)

    def ask_validate(self):
        if self.id:
            answer = self.ask_yes_no_question("Validate order")
            if answer is True:
                self.__validate__()
