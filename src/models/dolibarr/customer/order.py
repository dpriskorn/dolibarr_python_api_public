from datetime import datetime

from src.models.basemodels.my_base_model import MyBaseModel


class DolibarrCustomerOrder(MyBaseModel):
    """Models a customer order in Dolibarr.
    Defaults to SEK and Tradera account for payments"""

    # Optional
    id: int = 0
    thirdparty_id: int = 0
    customer_order_ref: str = ""
    multicurrency_code: str = "SEK"
    multicurrency_tx: int = 1  # currency_conversion_rate
    date: datetime = None

    def url(self):
        return f"{self._base_url}commande/card.php?id={self.id}"
