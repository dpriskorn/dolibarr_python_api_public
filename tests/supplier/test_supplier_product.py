from unittest import TestCase


class TestSupplierProduct(TestCase):
    pass
    # def test_get_already_imported_dolibarr_product(self):
    #     sp = MessingschlagerProduct(
    #         codename=SupportedSupplier.MESSINGSCHLAGER,
    #         product_category=ProductCategory.BIKE,
    #         sku=0,
    #     )
    #     result = sp.__get_already_imported_dolibarr_product__()
    #     assert result is None
    #     sp.dolibarr_product_id = FreightProductId.MESSINGSCHLAGER.value
    #     result2 = sp.__get_already_imported_dolibarr_product__()
    #     assert result2 is not None
    #     assert result2.ref == "frakt-ms"
    #     # assert result2.expired == Expired.FALSE
    #     assert result2.status_sell == Status.DISABLED
    #     assert result2.status_buy == Status.ENABLED
    #     assert result2.id == FreightProductId.MESSINGSCHLAGER.value
