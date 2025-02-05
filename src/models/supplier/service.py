from src.interfaces.reference import ReferenceInterface
from src.models.supplier.entity import SupplierEntity
from src.models.supplier.enums import EntityType


class SupplierService(SupplierEntity, ReferenceInterface):
    """This is not an abstract model. We use it for all supplier services for now"""

    # Mandatory
    reference: str

    entity_type: EntityType = EntityType.SERVICE

    def generated_url(self):
        pass

    def update_and_import_if_missing(self):
        pass

    def update_purchase_price(self):
        pass

    def generated_dolibarr_ref(self):
        return f"{self.codename.value}-{self.reference}"
