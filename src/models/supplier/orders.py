import logging
from abc import ABC, abstractmethod
from typing import List

from requests import Session

from src.models.basemodels.my_base_model import MyBaseModel
from src.models.supplier.order import SupplierOrder

logger = logging.getLogger(__name__)


class SupplierOrders(MyBaseModel, ABC):
    orders: List[SupplierOrder] = []
    session: Session

    @abstractmethod
    def __fetch__(self):
        pass

    @abstractmethod
    def __parse__(self):
        pass

    def import_all(self):
        self.__fetch__()
        self.__parse__()
        for order in self.orders:
            # print(type(order))
            # exit()
            if not isinstance(order, SupplierOrder):
                raise ValueError("not a supplier order child class")
            order.import_order()
            if order.dolibarr_supplier_order is not None:
                order.import_invoice()
