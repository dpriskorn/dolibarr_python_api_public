from abc import ABC, abstractmethod

from src.models.dolibarr.enums import Currency
from src.models.supplier.order import SupplierOrder


class SupplierEuOrder(SupplierOrder, ABC):
    """Class with currency EUR as standard"""

    currency: Currency = Currency.EUR
    # None of our EU supplier have free freight ever
    free_freight: bool = False
    # We always want to manually handle payments
    insert_payment: bool = False

    @abstractmethod
    def url(self):
        raise NotImplementedError("Implement this in the subclass")
