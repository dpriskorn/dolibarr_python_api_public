import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from src.models.basemodels.my_base_model import MyBaseModel
from src.models.dolibarr.enums import Currency
from src.models.exceptions import MissingInformationError
from src.models.supplier.enums import EntityType, ProductCategory
from src.models.suppliers.enums import SupportedSupplier
from src.models.vat_rate import VatRate

logger = logging.getLogger(__name__)


class SupplierEntity(MyBaseModel, ABC):
    """Abstract class for entities in Dolibarr"""

    accountancy_code_buy: str = "4000"
    accountancy_code_sell: str = "3000"
    codename: Optional[SupportedSupplier] = None
    cost_price: float = 0.0
    description: str = ""
    dolibarr_product_id: int = 0
    entity_type: EntityType
    eur_cost_price: float = 0.0
    image_url: str = ""
    label: str = ""
    product_category: ProductCategory | None = None
    purchase_vat_rate: VatRate = VatRate.TWENTYFIVE
    dolibarr_ref: str = ""  # this is the reference used in Dolibarr
    selling_vat_rate: VatRate = VatRate.TWENTYFIVE
    url: str = ""

    def __get_already_imported_dolibarr_product__(self) -> Optional[Any]:
        """Get by id if set or fall back to getting by external ref and codename"""
        logger.debug("__get_already_imported_dolibarr_product__: Running")
        # if not self.ref:
        #     raise MissingInformationError("self.ref was None")
        if not self.codename:
            raise MissingInformationError("self.codename was None")
        from src.models.dolibarr.product import DolibarrProduct

        p = DolibarrProduct(api=self.api, supplier_product=self)  # base_url=base_url,
        if self.dolibarr_product_id:
            logger.debug("getting by id")
            p.id = self.dolibarr_product_id
            return p.get_by_id()  # typing: ignore # mypy: ignore
        else:
            logger.debug("getting by external ref")
            return p.get_by_external_ref(
                external_ref=str(self.reference) or "",
                codename=self.codename,
            )

    # TODO base this on entity instead
    def convert_to_dolibarr_product(self):
        logger.debug("convert_to_dolibarr_product: Running")
        from src.models.dolibarr.product import DolibarrProduct

        p = DolibarrProduct(supplier_product=self)
        p = p.lookup_from_supplier_product()
        if (
            p is not None
            and p.currency != Currency.SEK
            and not p.multicurrency_cost_price
        ):
            raise MissingInformationError(
                f"missing multicurrency_cost_price on "
                f"non-SEK product: {self.label}. "
            )
        return p

    @abstractmethod
    def update_and_import_if_missing(self):
        pass

    @abstractmethod
    def update_purchase_price(self):
        pass

    @abstractmethod
    def generated_url(self):
        pass
