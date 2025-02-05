import logging
from abc import abstractmethod
from typing import Any, Optional

from src.models.basemodels.my_base_model import MyBaseModel
from src.models.suppliers.enums import SupportedSupplier

logger = logging.getLogger(__name__)


class DolibarrEntity(MyBaseModel):
    """This is the parent class for DolibarrProduct and DolibarrService"""

    @abstractmethod
    def lookup_from_supplier_product(self) -> Optional[Any]:
        """This method looks up the product in Dolibarr and returns it if found"""

    @abstractmethod
    def get_by_id(self) -> Any:
        """This does not update the current product,
        but instead returns a new instance"""

    @abstractmethod
    def get_by_external_ref(
        self, codename: SupportedSupplier, external_ref: str
    ) -> Optional[Any]:  # type here is DolibarrProduct but setting it gives an error
        """Get product by internal external_ref if it exist and return DolibarrProduct"""
