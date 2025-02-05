from src.models.basemodels.my_base_model import MyBaseModel


class CartResponse(MyBaseModel):
    total_amount: float = 0.0
    on_stock: bool = True
