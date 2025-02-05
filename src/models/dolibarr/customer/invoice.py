import logging
from datetime import datetime
from typing import Any, List, Optional

from src.models.basemodels.my_base_model import MyBaseModel

logger = logging.getLogger(__name__)


class DolibarrCustomerInvoice(MyBaseModel):
    """This models a customer invoice in Dolibarrs datamodel

    #:param date: int
    #:param date_lim_reglement: int is the due date unix timestamp
    #:param socid: int is the id of the thirdparty in Dolibarr"""

    invoice_date: datetime = None
    due_date: datetime = None
    date: Optional[int] = None
    date_lim_reglement: Optional[int] = None
    fully_paid: bool = False
    id: int = 0
    label: str = ""
    lines: List[Any] = []  # typing: DolibarrLine
    ref: str = ""
    socid: int = 0
    payments: List[Any] = []  # typing: DolibarrCustomerPayment
    validated: bool = False

    @property
    def datetime_date(self):
        return datetime.fromtimestamp(self.date)

    @property
    def url(self):
        return f"{self._base_url}/compta/facture/card.php?facid={self.id}"

    def __calculate_line_prices__(self):
        """Calculate prices for all the lines"""
        [line.calculate_sales_line_prices() for line in self.lines]

    def set_timestamp_dates(self, date: datetime = None) -> None:
        """This set the two visible dates in Dolibarr"""
        if date is None:
            date = self.invoice_date
        self.date = self.date_lim_reglement = int(datetime.timestamp(date))
