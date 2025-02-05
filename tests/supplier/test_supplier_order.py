import logging
from datetime import datetime, timezone
from unittest import TestCase

import config
from src.models.suppliers.enums import SupplierBaseUrl, SupportedSupplier
from src.models.suppliers.hoj24.order import Hoj24Order

logging.basicConfig(level=config.loglevel)


class TestSupplierOrder(TestCase):
    def test___get_dolibarr_supplier__(self):
        so = Hoj24Order(
            base_url=SupplierBaseUrl.HOJ24,
            codename=SupportedSupplier.HOJ24,
            reference=0,
            delivery_date=datetime.now(tz=timezone.utc),
        )
        so.__get_dolibarr_supplier__()
        print(so.dolibarr_supplier.id)
        assert so.dolibarr_supplier.id == 694

    # def test___prepare_for_import_of_order__(self):
    #     so = MessingschlagerOrder(
    #         base_url=SupplierBaseUrl.MESSINGSCHLAGER,
    #         codename=SupportedSupplier.MESSINGSCHLAGER,
    #         order_date=datetime.now(timezone.utc),
    #         reference="test",
    #         file_path="",
    #     )
    #     so.rows.append(
    #         MessingschlagerOrderRow(
    #             entity=MessingschlagerProduct(sku=466008, eur_cost_price=0.15),
    #             quantity=1,
    #         )
    #     )
    #     so.__prepare_for_import_of_order__()

    def test__check_if_already_imported__(self):
        order = Hoj24Order(
            base_url=SupplierBaseUrl.HOJ24,
            codename=SupportedSupplier.HOJ24,
            reference="4653290",
            delivery_date=datetime.now(tz=timezone.utc),
        )
        order.__check_if_already_imported__()
        assert order.imported is True
