from typing import Any, Optional

from src.models.dolibarr.line import DolibarrLine


class DolibarrSupplierOrderLine(DolibarrLine):
    order: Optional[Any] = None  # typing: SupplierOrder # we only need the id from it
    round_up: bool = False
