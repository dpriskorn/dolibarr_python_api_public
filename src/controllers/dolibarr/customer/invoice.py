import logging
from datetime import datetime

import config
from config.enums import AccountId, PaymentSource
from src.controllers.dolibarr.customer.payment import DolibarrCustomerPaymentContr
from src.controllers.my_base_contr import MyBaseContr
from src.helpers import utilities
from src.models.dolibarr import DolibarrEndpoint
from src.models.dolibarr.customer.invoice import DolibarrCustomerInvoice
from src.models.exceptions import DolibarrError, MissingInformationError

logger = logging.getLogger(__name__)


class DolibarrCustomerInvoiceContr(MyBaseContr, DolibarrCustomerInvoice):
    def __import_invoice__(self) -> None:
        result = self.api.call_create_api(
            endpoint=DolibarrEndpoint.INVOICES,
            params=dict(
                ref_client=self.ref,
                date=datetime.timestamp(self.invoice_date),
                due_date=datetime.timestamp(self.due_date),
                note="Inserted with Python",
                socid=self.socid,
                label=self.label,
            ),
        )
        if result.status_code == 200:
            self.id = self.response_to_int_or_fail(result.text)
            logger.info(f"Invoice created, see {self.url}")
        else:
            raise DolibarrError(result.text)

    def __import_lines__(self):
        """Import the lines to the customer invoice"""
        logger.debug("Importing the lines")
        self.__calculate_line_prices__()
        for line in self.lines:
            vat_src_code = line.vat_src_code
            line_data = {
                # not present on lines for some reason so we take it from the order
                "socid": self.socid,
                "qty": line.quantity,
                "pu_ht": line.product.cost_price,
                "tva_tx": line.product.sales_vat_rate.value,
                "fk_product": line.product.id,
                "product_type": line.product.type.value,
                "multicurrency_subprice": line.multicurrency_subprice,
                "multicurrency_total_ttc": line.multicurrency_total_ttc,
                "multicurrency_total_ht": line.multicurrency_total_ht,
                # not supported because of bug #14404
                "vat_src_code": vat_src_code,
            }
            result = self.api.call_create_api(
                custom_endpoint=f"invoices/{self.id}/lines", params=line_data
            )
            if result.status_code == 200:
                logger.info(f"Line added, see {self.url}")
            else:
                raise DolibarrError(result.text)
        print(f"All {len(self.lines)} lines added succesfully")

    def create(self):
        """Create an invoice based on the object"""
        # For now we only support importing an invoice with lines
        if not self.lines:
            raise MissingInformationError("self.lines was empty")
        self.__import_invoice__()
        self.__import_lines__()

    def insert_payment_with_full_amount(
        self, payment_source: PaymentSource = None, date: datetime = None
    ):
        """Insert payment on invoice"""
        logger.info("Inserting payment without asking for confirmation")
        if not payment_source:
            raise ValueError("Got no payment source")
        if not date:
            # Default to invoice date
            logger.info("Got no payment date. Defaulting to invoice date")
            date = self.datetime_date

        payment = DolibarrCustomerPaymentContr(
            invoice=self,
            date=date,
            payment_source=payment_source,
            account_id=AccountId.SEB,
        )
        payment.create_with_full_amount()
        self.fully_paid = True
        if not self.payments:
            self.payments = []
        self.payments.append(payment)

    def validate_invoice(self):
        r = self.api.call_create_api(
            custom_endpoint=f"{DolibarrEndpoint.INVOICES.value}/{self.id}/validate",
        )
        utilities.print_result(
            r,
            "Invoice validated",
            "validating invoice",
        )
        self.validated = True

    def update_dates_on_invoice(self):
        self.set_timestamp_dates()
        # Generate the new params for upload and exclude those not set or neccessary
        params = self.model_dump(include={"date", "date_lim_reglement"})
        if config.loglevel == logging.DEBUG:
            print(params)
        self.api.call_update_api(
            endpoint=DolibarrEndpoint.INVOICES, object_id=self.id, params=params
        )
