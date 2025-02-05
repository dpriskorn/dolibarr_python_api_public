from src.models.supplier.order_row import SupplierOrderRow
from src.models.suppliers.shimano.product import ShimanoProduct


class ShimanoOrderRow(SupplierOrderRow):
    entity: ShimanoProduct
