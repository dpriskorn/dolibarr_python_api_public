from datetime import datetime
from typing import Any

from config.enums import AccountId, PaymentSource
from src.models.basemodels.my_base_model import MyBaseModel


class DolibarrSupplierPayment(MyBaseModel):
    account_id: AccountId
    date: datetime
    invoice: Any  # DolibarrSupplierInvoice
    payment_source: PaymentSource
