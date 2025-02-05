from unittest import TestCase

from src.models.exceptions import MissingInformationError
from src.models.suppliers.shimano.login import ShimanoLogin
from src.models.suppliers.shimano.product.search_endpoint import (
    ShimanoProductSearchEndpoint,
)
from src.models.suppliers.shimano.product.search_product import ShimanoSearchProduct


class TestSearchEndpoint(TestCase):
    session = ShimanoLogin().login_and_get_session()

    def test_body(self):
        """rm35 body"""
        if not self.session:
            raise MissingInformationError()
        so = ShimanoProductSearchEndpoint(
            product_code="Y3TE98040", session=self.session
        )
        product = so.get()
        assert isinstance(product, ShimanoSearchProduct)
        assert product.net_cost_price == 137.0
        assert product.recommended_sales_price == 249.0
        assert product.lead_time >= 5
        assert product.name == "Frihjulsbody enhet FH-RM35"

    def test_get_vevparti(self):
        if not self.session:
            raise MissingInformationError()
        so = ShimanoProductSearchEndpoint(
            product_code="EFCTY501C888CLB", session=self.session
        )
        product = so.get()
        assert isinstance(product, ShimanoSearchProduct)
        assert product.net_cost_price == 187.0
        assert product.recommended_sales_price == 349.0
        assert product.name == "SHIMANO Vevparti FC-TY501 8/7/6-delat"
