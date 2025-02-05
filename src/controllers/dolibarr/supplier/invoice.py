import logging
from datetime import datetime
from typing import Optional

from config.enums import AccountId, PaymentSource
from src.controllers.my_base_contr import MyBaseContr
from src.helpers import utilities
from src.models.dolibarr import DolibarrEndpoint
from src.models.dolibarr.enums import DolibarrTable
from src.models.dolibarr.supplier.invoice import DolibarrSupplierInvoice
from src.models.exceptions import DolibarrError, MissingInformationError

logger = logging.getLogger(__name__)


class DolibarrSupplierInvoiceContr(MyBaseContr, DolibarrSupplierInvoice):
    """This class control all CUD operations in Dolibarr"""

    def create_invoice(self) -> None:
        """Create new invoice in Dolibarr
        We don't ask the user before creating the invoice because
        they already approved the order"""
        if self.dolibarr_supplier_order:
            logger.info("Creating invoice based on order already in Dolibarr.")
            if not self.invoice_date:
                logger.debug("Defaulting to order date as invoice date")
                self.invoice_date = self.dolibarr_supplier_order.date
            if self.external_ref:
                logger.debug("Got external_ref argument")
            else:
                if self.dolibarr_supplier_order.external_ref:
                    logger.info(
                        f"Got no external_ref so we use '{self.dolibarr_supplier_order.external_ref}' from the order"
                    )
                    self.external_ref = self.dolibarr_supplier_order.external_ref
                else:
                    raise ValueError(
                        "Got no external_ref argument and could not set from order"
                    )
            self.__create_from_order__()
        else:
            logger.info("Creating invoice from object data.")
            result = self.api.call_create_api(
                endpoint=DolibarrEndpoint.SUPPLIER_INVOICE,
                params=dict(
                    ref_supplier=self.external_ref,
                    date=datetime.timestamp(self.invoice_date),
                    due_date=datetime.timestamp(self.due_date),
                    note="Inserted with Python",
                    socid=self.socid,
                    multicurrency_code=self.currency.value,
                    label=self.label,
                ),
            )
            if result.status_code == 200:
                self.id = self.response_to_int_or_fail(result.text)
                [line.calculate_purchase_line_prices() for line in self.lines]
                self.__import_lines__()
                logger.info(f"Invoice created, see {self.url}")
            else:
                raise DolibarrError(result.text)

    def insert_payment_with_full_amount(
        self,
        payment_source: PaymentSource = None,
        account_id: AccountId = AccountId.SEB,
        date: Optional[datetime] = None,
    ):
        """Insert payment on invoice"""
        logger.info("Inserting payment without asking for confirmation")
        if not payment_source:
            raise ValueError("Got no payment source")
        if not date:
            # Default to invoice date
            logger.info("Got no payment date. Defaulting to invoice date")
            date = self.invoice_date

        from src.controllers.dolibarr.supplier.payment import (
            DolibarrSupplierPaymentContr,
        )

        payment = DolibarrSupplierPaymentContr(
            invoice=self,
            date=date,
            payment_source=payment_source,
            account_id=account_id,
        )
        payment.create_with_full_amount()
        self.fully_paid = True
        if not self.payments:
            self.payments = []
        self.payments.append(payment)

    def validate_invoice(self):
        r = self.api.call_create_api(
            custom_endpoint=f"supplierinvoices/{self.id}/validate",
        )
        utilities.print_result(
            r,
            "Supplier invoice validated",
            "validating supplier invoice",
        )
        self.validated = True

    def __create_from_order__(self):
        if not self.dolibarr_supplier_order.lines:
            raise ValueError("self.order.lines was None")
        if not self.dolibarr_supplier_order.id:
            raise ValueError("self.order.id was None")
        data = {
            "external_ref": "auto",
            "ref_supplier": self.dolibarr_supplier_order.ref,
            "socid": self.dolibarr_supplier_order.supplier_order.dolibarr_supplier.id,
            "note": "Inserted with Python",
            "order_supplier": self.dolibarr_supplier_order.id,
            "date": self.convert_datetime_to_iso(date=self.invoice_date),
        }
        # Insert supplier invoice
        response = self.api.call_create_api(
            endpoint=DolibarrEndpoint.SUPPLIER_INVOICE, params=data
        )
        self.id = self.response_to_int_or_fail(response.text)
        for line in self.dolibarr_supplier_order.lines:
            vat_src_code = line.vat_src_code
            line_data = {
                # not present on lines for some reason so we take it from the order
                "socid": self.dolibarr_supplier_order.id,
                "qty": line.quantity,
                "pu_ht": line.product.cost_price,
                "tva_tx": line.product.purchase_vat_rate.value,
                "fk_product": line.product.id,
                "product_type": line.product.type.value,
                "remise_percent": self.dolibarr_supplier_order.supplier_order.discount_percentage,
                # not supported because of bug #14404
                "vat_src_code": vat_src_code,
            }
            response = self.api.call_create_api(
                custom_endpoint=f"supplierinvoices/{self.id}/lines", params=line_data
            )
            # TODO test this
            if vat_src_code != "":
                logger.debug(f"Inserting vat_src_code {vat_src_code} into Dolibarr")
                # Add id to object
                line.id = self.response_to_int_or_fail(response.text)
                logger.debug(f"Got line id: {line.id}")
                if line.id:
                    self.update.update_vat_src_code_on_supplier_invoice_line(
                        line=line,
                    )
        print(f"Inserted supplier invoice, see {self.url}")
        # TODO support multiple orders linked to 1 invoice (SH)

        self.create.insert_link(
            fk_source=self.dolibarr_supplier_order.id,
            source_table=DolibarrTable.SUPPLIER_ORDER,
            fk_target=self.id,
            target_table=DolibarrTable.SUPPLIER_INVOICE,
        )
        self.linked = True

    def __import_lines__(self):
        """We import all lines"""
        for line in self.lines:
            if not line.product:
                raise MissingInformationError()
            if not line.product.purchase_vat_rate:
                raise MissingInformationError(
                    f"line.product.purchase_vat_rate was None, "
                    f"see {line.product.selling_price_url}"
                )
            vat_src_code = line.vat_src_code
            line_data = {
                # not present on lines for some reason so we take it from the order
                "socid": self.socid,
                "qty": line.quantity,
                "pu_ht": line.product.cost_price,
                "tva_tx": line.product.purchase_vat_rate.value,
                "fk_product": line.product.id,
                "product_type": line.product.type.value,
                "multicurrency_subprice": line.multicurrency_subprice,
                "multicurrency_total_ttc": line.multicurrency_total_ttc,
                "multicurrency_total_ht": line.multicurrency_total_ht,
                # not supported because of bug #14404
                "vat_src_code": vat_src_code,
            }
            result = self.api.call_create_api(
                custom_endpoint=f"supplierinvoices/{self.id}/lines", params=line_data
            )
            if result.status_code == 200:
                logger.info(f"Line added, see {self.url}")
            else:
                raise DolibarrError(result.text)
        print(f"All {len(self.lines)} lines added succesfully")
