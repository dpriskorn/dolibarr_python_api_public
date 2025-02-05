from unittest import TestCase

from pydantic import ValidationError

from src.models.dolibarr.enums import Expired
from src.models.exceptions import NotFoundError
from src.models.suppliers.enums import SupplierBaseUrl
from src.models.suppliers.messingschlager.product import MsProduct
from src.models.vat_rate import VatRate


class MessingschlagerProductTests(TestCase):
    def test_ref_none(self):
        with self.assertRaises(ValidationError):
            MsProduct(sku=None)  # type: ignore

    @staticmethod
    def test_ref_too_short():
        msp = MsProduct(sku=1)
        assert msp.__valid_sku__() is False
        msp = MsProduct(sku=11111)
        assert msp.__valid_sku__() is False

    @staticmethod
    def test_ref_too_long():
        msp = MsProduct(sku=1111111)
        assert msp.__valid_sku__() is False

    @staticmethod
    def test_ref_valid():
        msp = MsProduct(sku=111111)
        assert msp.__valid_sku__() is True

    @staticmethod
    def test_scrape_product_valid_ref():
        msp = MsProduct(sku=130097)
        assert msp.scraped is False
        assert msp.cost_price == 0
        msp.scrape_product()
        assert msp.eur_cost_price > 2.0
        assert msp.eur_list_price > 6.0
        assert msp.expired == Expired.FALSE
        assert (
            msp.image_url
            == f"{SupplierBaseUrl.MESSINGSCHLAGER.value}content/Artikelfotos/130097_100520.jpg"
        )
        assert msp.label_en == "VENTURA saddle cover"
        assert (
            msp.label_de
            == "Regenüberzug VENTURA für Sattel, Universalgröße, mit Bandero"
        )
        assert msp.purchase_vat_rate == VatRate.ZERO
        assert msp.selling_vat_rate == VatRate.TWELVE
        assert msp.sku == 130097
        assert msp.available is False
        # We never get restock dates for available products
        assert msp.restock_date is None
        # print(msp.dict())

    def test_scrape_product_invalid_ref(self):
        msp = MsProduct(sku=111111)
        with self.assertRaises(NotFoundError):
            msp.scrape_product()
