from unittest import TestCase

from src.models.dolibarr.enums import Currency, Expired, Status
from src.models.suppliers.enums import SupportedSupplier
from src.models.suppliers.hoj24.product import Hoj24Product
from src.models.vat_rate import VatRate
from src.views.dolibarr.product import DolibarrProductView


class TestDolibarrProductView(TestCase):
    def test_dolibarr_product_view_no_supplier_product(self):
        dpv = DolibarrProductView(testing=True)
        with self.assertRaises(ValueError):
            dpv.__prepare_before_creating_new_product__()

    def test_dolibarr_product_view_bike_supplier_product(self):
        dpv = DolibarrProductView(testing=True, supplier_product=Hoj24Product(sku="1"))
        dpv.__prepare_before_creating_new_product__()
        assert dpv.accountancy_code_buy == "4000"
        assert dpv.accountancy_code_sell == "3001"
        assert dpv.codename == SupportedSupplier.HOJ24
        assert dpv.cost_price == 0
        assert dpv.expired == Expired.FALSE
        assert dpv.external_image_url == ""
        assert dpv.external_url == ""
        # assert dpv.last_update == ""
        assert dpv.ref == "JO-1"
        assert dpv.sales_vat_rate == VatRate.TWELVE
        assert dpv.sku == "1"
        assert dpv.status_buy == Status.ENABLED
        assert dpv.currency == Currency.SEK
