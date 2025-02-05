from abc import ABC, abstractmethod

from src.models.supplier.enums import ProductCategory
from src.models.supplier.product import SupplierProduct
from src.models.vat_rate import VatRate


class BikeProduct(SupplierProduct, ABC):
    """Abstract model for any bike product at a supplier

    The vat rate differs from the supplier product and the
    dolibarr product because we pay 25% VAT on purchase but
    sell repair services incl. products that gets mounted
    on the bikes is 12% VAT since mid 2023"""

    product_category: ProductCategory = ProductCategory.BIKE
    selling_vat_rate: VatRate = VatRate.TWELVE
    accountancy_code_sell: str = "3001"

    @abstractmethod
    def __scrape_product__(self):
        raise NotImplementedError("Implement this in the subclass")
