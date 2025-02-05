import logging
from typing import Optional

from src.models.basemodels.my_base_model import MyBaseModel
from src.models.dolibarr.enums import Currency
from src.models.dolibarr.product import DolibarrProduct
from src.models.exceptions import MissingInformationError
from src.models.vat_rate import VatRate

logger = logging.getLogger(__name__)


class DolibarrLine(MyBaseModel):
    """This model a line on Dolibarr objects like invoice and order"""

    id: Optional[int] = None
    # bought_quantity: Optional[int]
    # cost_price: Optional[float]
    multicurrency_subprice: float = 0.0
    multicurrency_total_ttc: float = 0.0
    multicurrency_total_ht: float = 0.0
    # From Product we get:
    # OOP attributes vs Dolibarr
    # bought_quantity = qty
    # id = fk_product
    # currency = multicurrency_code
    # type = product_type
    # purchase_vat_rate = tva_tx

    # We get a Pydantic error so we use Any here
    product: "DolibarrProduct"  # type : DolibarrProduct
    total_ht: Optional[float] = None
    total_ttc: Optional[float] = None
    total_tva: Optional[float] = None
    vat_src_code: Optional[str] = ""
    quantity: int
    round_up: bool = False

    def __calculate_purchase_tax_multiplier__(self):
        """Calculate the tax multiplier we need"""

        # if not isinstance(self, DolibarrSupplierOrderLine):
        #     raise NotImplementedError(
        #         "Calculating line prices is currently "
        #         "only supported for supplier order lines"
        #     )
        # If no tax, multiply by one instead
        # self.product: DolibarrProduct
        if not self.product.purchase_vat_rate:
            if self.product.currency == Currency.EUR:
                self.product.purchase_vat_rate = VatRate.ZERO
            else:
                self.product.purchase_vat_rate = VatRate.TWENTYFIVE
        if self.product.purchase_vat_rate != VatRate.ZERO:
            tax_multiplier = 1 + (self.product.purchase_vat_rate.value / 100)
        elif self.product.purchase_vat_rate == VatRate.ZERO:
            tax_multiplier = 1.0
        else:
            raise ValueError(
                f"Tax multiplier could not be calculated based on {self.product.purchase_vat_rate}"
            )
        logger.debug(f"Supplier VAT: {self.product.purchase_vat_rate}")
        logger.debug(f"using tax_multiplier: {tax_multiplier}")
        return tax_multiplier

    def __calculate_sales_tax_multiplier__(self):
        """Calculate the tax multiplier we need"""

        # if not isinstance(self, DolibarrSupplierOrderLine):
        #     raise NotImplementedError(
        #         "Calculating line prices is currently "
        #         "only supported for supplier order lines"
        #     )
        # If no tax, multiply by one instead
        # self.product: DolibarrProduct
        if not self.product.sales_vat_rate:
            raise ValueError(
                f"self.product.purchase_vat_rate on {self.product.label}: {self.product.url} was None"
            )
        if self.product.sales_vat_rate != VatRate.ZERO:
            # noinspection PyTypeChecker
            tax_multiplier = 1 + (self.product.purchase_vat_rate.value / 100)
        elif self.product.sales_vat_rate == VatRate.ZERO:
            tax_multiplier = 1.0
        else:
            raise ValueError(
                f"Tax multiplier could not be calculated based on {self.product.purchase_vat_rate}"
            )
        logger.debug(f"Customer VAT: {self.product.sales_vat_rate}")
        logger.debug(f"using tax_multiplier: {tax_multiplier}")
        return tax_multiplier

    def calculate_purchase_line_prices(self):
        logger.debug("calculate_purchase_line_prices: Running")
        logger.info("Calculating line prices")
        tax_multiplier = self.__calculate_purchase_tax_multiplier__()
        if self.product.currency != Currency.SEK:
            if not self.product.multicurrency_cost_price:
                raise MissingInformationError(
                    "multicurrency_cost_price was None on product: "
                    f"{self.product.label}"
                )
            if not self.quantity:
                raise MissingInformationError("quantity was None")
            if not tax_multiplier:
                raise MissingInformationError("tax_multiplier was None")
            logger.debug("Calculating multicurrency prices")
            self.multicurrency_total_ttc = (
                self.product.multicurrency_cost_price * self.quantity * tax_multiplier
            )
            self.multicurrency_total_ht = (
                self.product.multicurrency_cost_price * self.quantity
            )
        else:
            logger.debug("Skipping calculation of multicurrency prices")
        if not self.product.purchase_price_found:
            # workaround
            logger.warning(
                f"No purchase price found for this product, see product id: {self.product.id}"
            )
            # DISABLED because of weird pydantic bug
            # E       AttributeError: 'DolibarrProduct' object has no attribute '_DolibarrProduct__base_url'
            # logger.warning(
            #     f"No purchase price found for this product, see {self.product.url}"
            # )
        if not self.quantity:
            raise MissingInformationError("quantity was None")
        if not self.product.cost_price:
            if self.product.currency == Currency.SEK:
                # print(self.product)
                raise MissingInformationError(
                    f"cost price was None on this product: {self.product.label}, see {self.product.url} and {self.product.dolibarr_product_url}"
                )
            else:
                self.product.__calculate_sek_prices_from_eur__()
        # if self.round_up:
        #     self.total_ttc = numpy.ceil(
        #         self.product.cost_price * self.quantity * tax_multiplier
        #     )
        #     self.total_ht = numpy.ceil(self.product.cost_price * self.quantity)
        #     self.total_tva = numpy.ceil(
        #         self.total_ht * (tax_multiplier - 1)
        #     )  # x0.25 total vat
        # else:
        self.total_ttc = self.product.cost_price * self.quantity * tax_multiplier
        self.total_ht = self.product.cost_price * self.quantity
        self.total_tva = self.total_ht * (tax_multiplier - 1)  # x0.25 total vat
        # TODO what about multicurrency sums?

    def calculate_sales_line_prices(self):
        logger.debug("calculate_line_prices: Running")
        logger.info("Calculating line prices")
        if not self.quantity:
            raise MissingInformationError("quantity was None")
        if not self.product.cost_price:
            raise MissingInformationError("cost price was None")
        tax_multiplier = self.__calculate_sales_tax_multiplier__()
        self.total_ttc = self.product.cost_price * self.quantity * tax_multiplier
        self.total_ht = self.product.cost_price * self.quantity
        self.total_tva = self.total_ht * (tax_multiplier - 1)  # x0.25 total vat
        if self.product.currency != Currency.SEK:
            if not self.product.multicurrency_sales_price:
                raise MissingInformationError(
                    "self.product.multicurrency_sales_price was None"
                )
            self.multicurrency_subprice = self.product.multicurrency_sales_price
            if not self.product.multicurrency_cost_price:
                raise ValueError("multicurrency_cost_price was None")
            logger.debug("Calculating multicurrency prices")
            self.multicurrency_total_ttc = (
                self.product.multicurrency_cost_price * self.quantity * tax_multiplier
            )
            self.multicurrency_total_ht = (
                self.product.multicurrency_cost_price * self.quantity
            )
        else:
            logger.debug("Skipping calculation of multicurrency prices")
            self.multicurrency_total_ttc = 0
            self.multicurrency_total_ht = 0
