import logging
from datetime import datetime
from typing import TYPE_CHECKING

from config.enums import AccountId, PaymentSource
from src.models.basemodels.my_base_model import MyBaseModel

if TYPE_CHECKING:
    from src.models.dolibarr.customer.invoice import DolibarrCustomerInvoice

logger = logging.getLogger(__name__)


class DolibarrCustomerPayment(MyBaseModel):
    account_id: AccountId
    date: datetime
    invoice: "DolibarrCustomerInvoice"
    payment_source: PaymentSource
