import logging
from abc import ABC
from datetime import datetime

from src.models.basemodels.my_base_model import MyBaseModel
from src.models.dolibarr.enums import Currency
from src.models.exceptions import MissingInformationError
from src.models.supplier.entity import SupplierEntity

logger = logging.getLogger(__name__)


class SupplierOrderRow(MyBaseModel, ABC):
    quantity: int
    entity: SupplierEntity
    round_up: bool = False
    delivery_date: datetime | None = None
    model_config = {"extra": "forbid"}

    def to_dolibarr_order_line(self):
        logger.debug("to_dolibarr_order_line: Running")
        product = self.entity.convert_to_dolibarr_product()
        if not product:
            raise Exception(
                "Could not convert this line because the product does not exits in Dolibarr yet."
            )
        if not product.type:
            raise MissingInformationError("product type was None")
        if product.currency != Currency.SEK and not product.multicurrency_cost_price:
            raise MissingInformationError(
                f"missing multicurrency_cost_price on non-SEK product: {self.entity.label}. Entity is: {self.entity.model_dump()}"
            )
        # if not product.currency:
        #     raise ValueError("product.currency was None")
        from src.models.dolibarr.supplier.order_line import DolibarrSupplierOrderLine

        return DolibarrSupplierOrderLine(
            product=product, quantity=self.quantity, round_up=self.round_up
        )
