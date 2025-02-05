import logging
from typing import TYPE_CHECKING

from src.models.supplier.order_row import SupplierOrderRow

if TYPE_CHECKING:
    from src.models.suppliers.biltema import BiltemaProduct

logger = logging.getLogger(__name__)


class BiltemaOrderRow(SupplierOrderRow):
    entity: "BiltemaProduct"
    quantity: int = 0
