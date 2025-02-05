from datetime import datetime
from typing import Optional

from config.enums import AccountId, PaymentSource
from src.controllers.dolibarr.supplier.invoice import DolibarrSupplierInvoiceContr
from src.views.my_base_view import MyBaseView


class DolibarrSupplierInvoiceView(MyBaseView, DolibarrSupplierInvoiceContr):
    """This class controls all user interaction needed"""

    def ask_insert_payment_with_full_amount(
        self,
        account_id: AccountId = AccountId.SEB,
        payment_source: PaymentSource = None,
        date: Optional[datetime] = None,
    ) -> None:
        answer = self.ask_yes_no_question("Insert payment with full amount?")
        if answer is True:
            self.insert_payment_with_full_amount(
                payment_source=payment_source, date=date, account_id=account_id
            )
        else:
            return

    def ask_validate(self) -> None:
        answer = self.ask_yes_no_question("Validate invoice")
        if answer is True:
            self.validate_invoice()
        else:
            return
