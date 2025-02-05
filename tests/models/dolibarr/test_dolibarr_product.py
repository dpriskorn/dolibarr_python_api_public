import json
import logging
from unittest import TestCase

import config
from src.models.dolibarr.enums import Currency, StockType
from src.models.dolibarr.my_dolibarr_api import MyDolibarrApi
from src.models.dolibarr.product import DolibarrProduct
from src.models.exceptions import MissingInformationError
from src.models.suppliers.enums import SupportedSupplier
from src.models.vat_rate import VatRate

logging.basicConfig(level=config.loglevel)

# Specify the path to your JSON file
# TODO update to v19 product
file_path = "/home/dpriskorn/src/python/dolibarr_python_api/test_data/dolibarr_product_test_v14.json"

# Open the file and read its contents
with open(file_path) as json_file:
    # Load the JSON data
    mock_product_data = json.load(json_file)


class TestDolibarrProduct(TestCase):
    @staticmethod
    def test_getting_from_id_currency():
        # TODO mock data instead of testing on the production database
        p = DolibarrProduct(id=1246, api=MyDolibarrApi())
        p = p.get_by_id()
        p.fetch_purchase_data_and_finish_parsing()
        assert p.currency == Currency.SEK

    @staticmethod
    def test_get_by_id_correct_type():
        p = DolibarrProduct(id=1544, api=MyDolibarrApi())
        p = p.get_by_id()
        p.fetch_purchase_data_and_finish_parsing()
        assert p.type == StockType.SERVICE

    @staticmethod
    def test_getting_label():
        # TODO mock data instead of testing on the production database
        p = DolibarrProduct(id=1246, api=MyDolibarrApi())
        p = p.get_by_id()
        assert p.label == "Slang 16, 40/62-305, DV"

    # def test_create_new_product_with_valid_codename(self):
    #     # TODO create the product in Dolibarr and delete it afterwards
    #     p = BiltemaProduct(
    #         sku="test",
    #         codename=SupportedSupplier.BILTEMA,
    #         product_category=ProductCategory.BIKE,
    #     )
    #     # p.label = "test"
    #     # p.cost_price = 0
    #     # p.available = False
    #     # p.stock = 0
    #     # p.restock_date = datetime.now(tz=self.stockholm_timezone)
    #     # p.description = ""
    #     # p.image_url = ""
    #     # print(p)
    #     d = DolibarrProduct(supplier_product=p)
    #     # print(d)
    #     self.assertEqual(d.supplier_product.ref, "test")

    @staticmethod
    def test_get_by_external_ref_id():
        # TODO improve this to create a test product first
        dp = DolibarrProduct()
        # assert dp.api.database == Database.TESTING
        product = dp.get_by_external_ref(
            external_ref="ESM3C41NCL040E", codename=SupportedSupplier.SHIMANO
        )
        assert product.id == 1184
        # self.fail()

    @staticmethod
    def test_get_by_external_ref_id_currency_vat_rate():
        dp = DolibarrProduct(api=MyDolibarrApi())
        product: DolibarrProduct = dp.get_by_external_ref(
            external_ref="ESM3C41NCL040E", codename=SupportedSupplier.SHIMANO
        )
        product.fetch_purchase_data_and_finish_parsing()
        assert product.currency == Currency.SEK
        assert product.purchase_vat_rate == VatRate.TWENTYFIVE

    def test_lookup_from_supplier_product_no_product(self):
        dp = DolibarrProduct(api=MyDolibarrApi())
        with self.assertRaises(MissingInformationError):
            dp.lookup_from_supplier_product()

    # @staticmethod
    # def test_lookup_from_supplier_product_ms_product():
    #     """This test make sure that we pass on the price from eur_cost_price correctly"""
    #     dp = DolibarrProduct(
    #         supplier_product=MessingschlagerProduct(sku=466008, eur_cost_price=0.15),
    #         api=MyDolibarrApi(),
    #     )
    #     p = dp.lookup_from_supplier_product()
    #     assert p.multicurrency_cost_price == 0.15
    #     assert p.label == "Reflex fram med skruv"
    #     assert p.codename == SupportedSupplier.MESSINGSCHLAGER

    # @staticmethod
    # def test_lookup_from_supplier_product_ms_freight_service():
    #     """This test make sure that we pass on the price from eur_cost_price correctly"""
    #     dp = DolibarrProduct(
    #         supplier_product=SupplierService(
    #             dolibarr_product_id=int(FreightProductId.MESSINGSCHLAGER.value),
    #             eur_cost_price=0.1,
    #             purchase_vat_rate=VatRate.ZERO,
    #             codename=SupportedSupplier.MESSINGSCHLAGER,
    #             reference="",
    #         ),
    #         api=MyDolibarrApi(),
    #     )
    #     p = dp.lookup_from_supplier_product()
    #     assert p.multicurrency_cost_price == 0.1
    #     assert p.label == "Messingschlager frakt"
    #     # We don't need this on services
    #     assert p.codename is None

    @staticmethod
    def test_virtual_stock():
        # fixme run test
        #  is the endpoint reliable for this data in v19? It always returned null in v14.
        p = DolibarrProduct(**mock_product_data)
        assert p.virtual_stock == 2

    @staticmethod
    def test_external_ref_setter():
        p = DolibarrProduct(**mock_product_data)
        assert p.external_ref == "376482"
        p.external_ref = "test"
        assert p.external_ref == "test"

    @staticmethod
    def test_desired_stock_quantity_setter():
        p = DolibarrProduct(**mock_product_data)
        assert p.desired_stock_quantity == 0
        p.desired_stock_quantity = 1
        assert p.desired_stock_quantity == 1

    @staticmethod
    def test_stock_warning_quantity_setter():
        p = DolibarrProduct(**mock_product_data)
        assert p.stock_warning_quantity == 0
        p.stock_warning_quantity = 1
        assert p.stock_warning_quantity == 1

    def test_label_en(self):
        p = DolibarrProduct(**mock_product_data)
        assert p.label_en == ""
        p.label_en = "test"
        assert p.label_en == "test"

    # def test_label_de(self):
    #     p = DolibarrProduct(**mock_product_data)
    #     assert p.label_de == ""
    #     p.label_de = "test"
    #     assert p.label_de == "test"
