import logging
from unittest import TestCase

import config
from src.helpers.crud.read import Read
from src.models.suppliers.enums import SupportedSupplier

logging.basicConfig(level=config.loglevel)
logging.getLogger(__name__)


class TestRead(TestCase):
    read: Read = None

    def setUp(self):
        self.read = Read()

    def test_dolibarr_product_id_by_external_ref(self):
        product_id = self.read.get_dolibarr_product_id_by_external_ref(
            external_ref="251021", codename=SupportedSupplier.MESSINGSCHLAGER
        )
        assert product_id == 686

    def test_dolibarr_product_id_by_external_ref_not_exist(self):
        product_id = self.read.get_dolibarr_product_id_by_external_ref(
            external_ref="251021345677", codename=SupportedSupplier.MESSINGSCHLAGER
        )
        assert product_id == 0
