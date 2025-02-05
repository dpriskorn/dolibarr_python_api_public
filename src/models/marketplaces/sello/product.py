from datetime import datetime
from typing import Optional

from src.models.basemodels.my_base_model import MyBaseModel


class SelloProduct(MyBaseModel):
    created_at: datetime
    group_id: int
    id: int
    private_name: str
    private_reference: str
    purchase_price: Optional[float]
    quantity: int
    updated_at: datetime

    # class Config:
    #     extra = "forbid"
