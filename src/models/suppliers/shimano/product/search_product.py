from src.models.basemodels.my_base_model import MyBaseModel


class ShimanoSearchProduct(MyBaseModel):
    """This models a flattened json product from the ShimanoProductSearch endpoint"""

    baseProduct: str  # more detailed code with prefix
    basePrice_value: float
    stock_stockLevel: int
    baseProductName: str  # swedish name
    srpPrice_value: float  # this is the Shimano recommended price to end customer
    inStockFlag: bool
    leadTime: int  # days
    ean: str = ""

    @property
    def net_cost_price(self):
        return self.basePrice_value

    @property
    def recommended_sales_price(self):
        return self.srpPrice_value

    @property
    def name(self):
        return self.baseProductName

    @property
    def stock_level(self):
        return self.stock_stockLevel

    @property
    def lead_time(self) -> int:
        """Time in days"""
        return self.leadTime
