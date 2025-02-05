from typing import Any

from src.models.basemodels.my_base_model import MyBaseModel


class SelloOrderRow(MyBaseModel):
    """This models an order row from Sello
    reference is the dolibarr id of the product"""

    # This id is not trustable. It does not exist on the product endpoint.
    item_no: int
    reference: str | None
    quantity: int
    price: float
    title: str
    image: Any = None

    class Config:  # dead: disable
        extra = "ignore"

    @property
    def image_url(self) -> str:
        if self.image is not None:
            return str(self.image)
        else:
            return ""

    @property
    def gross_price(self) -> float:
        """Gross price"""
        return self.price

    @property
    def net_price(self) -> float:
        return self.price / 1.25

    @property
    def multicurrency_subprice(self) -> float:
        """Price without vat"""
        return round(self.net_price, 2)

    @property
    def dolibarr_reference(self) -> int:
        if self.reference is not None:
            return int(self.reference)
        else:
            raise ValueError("reference was None")

    # TODO move to new SelloOrderRowContr?
    def calculate_new_price_based_on_quantity(self):
        new_price = self.price / self.quantity
        print(f"New gross price calculated based on quantity: {round(new_price)}")
        self.price = new_price
