import logging
from abc import ABC
from datetime import datetime
from typing import Any, List, Optional

from src.models.basemodels.my_base_model import MyBaseModel
from src.models.dolibarr.enums import Currency
from src.models.dolibarr.supplier.invoice_line import DolibarrSupplierInvoiceLine
from src.models.dolibarr.supplier.payment import DolibarrSupplierPayment

logger = logging.getLogger(__name__)


class DolibarrSupplierInvoice(MyBaseModel, ABC):
    """This is an abstract model for a supplier invoice in Dolibarr

    We don't support linking multiple orders and invoices.
    That should only be done in the Web UI."""

    discount_percentage: float = 0.0
    dolibarr_supplier_order: Any  # cannot type this because of pydantic forward ref error "DolibarrSupplierOrderView"
    due_date: datetime
    fully_paid: bool = False
    id: int = 0
    invoice_date: Optional[datetime] = None
    label: str = ""
    lines: List["DolibarrSupplierInvoiceLine"] = []
    linked: bool = False
    payments: List["DolibarrSupplierPayment"] = []
    socid: int = 0
    validated: bool = False
    external_ref: str = ""
    currency: Currency = Currency.SEK

    @property
    def url(self):
        return f"{self._base_url}/fourn/facture/card.php?facid={self.id}"

    @staticmethod
    def convert_datetime_to_iso(date: datetime):
        return date.strftime("%Y-%m-%d")
