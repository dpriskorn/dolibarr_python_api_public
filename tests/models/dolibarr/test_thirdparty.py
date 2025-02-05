import logging
from unittest import TestCase

import config
from src.models.thirdparty import Thirdparty

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)


class TestThirdparty(TestCase):
    def test_find_thirdparty_customer_id_or_false(self):
        # TODO make this test work on a clean database
        t = Thirdparty(tradera_alias="divers")
        dolibarr_id = t.find_thirdparty_customer_id_by_tradera_alias_or_false()
        logger.info(f"id:{dolibarr_id}")
        if dolibarr_id is False:
            self.fail()
        assert dolibarr_id == 1013
