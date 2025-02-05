from abc import ABC, abstractmethod

from src.models.dolibarr.enums import Currency
from src.models.supplier.product.bike_product import BikeProduct


class SekBikeProduct(BikeProduct, ABC):
    """Abstract model for a bike product sold in SEK at a supplier"""

    currency: Currency = Currency.SEK

    @abstractmethod
    def __scrape_product__(self):
        raise NotImplementedError("Implement this in the subclass")

    @abstractmethod
    def __login__(self):
        raise NotImplementedError("Implement this in the subclass")
