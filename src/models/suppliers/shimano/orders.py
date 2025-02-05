from typing import List

from src.models.supplier.orders import SupplierOrders
from src.models.suppliers.shimano import ShimanoOrder


class ShimanoOrders(SupplierOrders):
    def __fetch__(self):
        pass

    def __parse__(self):
        pass

    orders: List[ShimanoOrder] = []
