from abc import ABC, abstractmethod

from src.models.supplier.product.bike_product import BikeProduct


class EuBikeProduct(BikeProduct, ABC):
    """Abstract model for a bike product from an EU supplier

    The vat rate differs from the supplier product and the
    dolibarr product because we pay 25% VAT on purchase but
    sell repair services incl. products that gets mounted
    on the bikes for 6% VAT"""

    accountancy_code_buy: str = "4535"
    eur_list_price: float = 0.0

    @abstractmethod
    def __scrape_product__(self):
        raise NotImplementedError("Implement this in the subclass")
