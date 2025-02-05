from unittest import TestCase

from src.models.suppliers.biltema import BiltemaOrder


class TestBiltemaOrder(TestCase):
    def test___get_existing_product__(self):
        biltema = BiltemaOrder()
        assert biltema.__get_existing_product__(ref="27-9906") is not None

    def test___get_order_row__(self):
        biltema = BiltemaOrder()
        assert biltema.__get_order_row__(ref="27-9906") is not None

    # def test_purchase(self):
    #     biltema = BiltemaOrder()
    #     # todo fix test
    #     biltema.import_purchase(refs=["27-9906"])
