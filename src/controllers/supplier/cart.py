from abc import ABC, abstractmethod

from src.controllers.my_base_contr import MyBaseContr
from src.models.supplier.product import SupplierProduct


class SupplierCartContr(MyBaseContr, ABC):
    """Abstract controller class for supplier cart"""

    @abstractmethod
    def add(self, product: SupplierProduct):
        """Method that adds to a supplier cart.
        Mandatory to implement"""
        raise NotImplementedError()
