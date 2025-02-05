import logging
from datetime import datetime
from unittest import TestCase

import config
from src.models.basemodels.my_base_model import MyBaseModel
from src.models.suppliers.hoj24.order import Hoj24Order

logging.basicConfig(level=config.loglevel)


class Hoj24OrderTests(TestCase):
    """Tests for the Hoj24Product class"""

    @staticmethod
    def test_instantiation():
        order = Hoj24Order(
            reference=1234,
            delivery_date=datetime.now(tz=MyBaseModel().stockholm_timezone),
        )
        assert order.reference == 1234
