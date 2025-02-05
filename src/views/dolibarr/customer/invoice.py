from datetime import datetime

from config.enums import PaymentSource
from src.controllers.dolibarr.customer.invoice import DolibarrCustomerInvoiceContr
from src.views.my_base_view import MyBaseView


class DolibarrCustomerInvoiceView(MyBaseView, DolibarrCustomerInvoiceContr):
    def ask_insert_payment_with_full_amount(
        self, payment_source: PaymentSource = None, date: datetime = None
    ) -> None:
        answer = self.ask_yes_no_question("Insert payment with full amount?")
        if answer is True:
            self.insert_payment_with_full_amount(
                payment_source=payment_source, date=date
            )
        else:
            return

    def ask_validate(self) -> None:
        answer = self.ask_yes_no_question("Validate invoice")
        if answer is True:
            self.validate_invoice()
        else:
            return
