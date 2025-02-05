from src.models.supplier.order_row import SupplierOrderRow
from src.models.suppliers.hoj24.product import Hoj24Product


class Hoj24OrderRow(SupplierOrderRow):
    entity: Hoj24Product
