from typing import Any, Optional

from src.models.dolibarr.entity import DolibarrEntity
from src.models.suppliers.enums import SupportedSupplier


class DolibarrService(DolibarrEntity):
    def lookup_from_supplier_product(self) -> Optional[Any]:
        raise NotImplementedError()

    def get_by_id(self) -> Any:
        raise NotImplementedError()

    def get_by_external_ref(
        self, codename: SupportedSupplier, external_ref: str
    ) -> Optional[Any]:
        raise NotImplementedError()
