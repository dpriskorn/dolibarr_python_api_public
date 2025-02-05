import logging

from src.controllers.my_base_contr import MyBaseContr
from src.helpers import utilities
from src.models.dolibarr.supplier.payment import DolibarrSupplierPayment

logger = logging.getLogger(__name__)


class DolibarrSupplierPaymentContr(MyBaseContr, DolibarrSupplierPayment):
    def create_with_full_amount(self):
        """This creates a payment on the full amount"""
        logger.debug(
            f"self.payment_source.value:{self.payment_source.value}, type: {type(self.payment_source.value)}"
        )
        data = dict(
            datepaye=self.date.timestamp(),
            # paiementid=self.payment_source.value,
            payment_mode_id=self.payment_source.value,
            closepaidinvoices="yes",
            accountid=self.account_id.value,
        )

        r = self.api.call_create_api(
            custom_endpoint=f"supplierinvoices/{self.invoice.id}/payments",
            params=data,
        )
        utilities.print_result(
            r,
            f"Supplier payment inserted with date {self.date}",
            "inserting supplier payment",
        )
