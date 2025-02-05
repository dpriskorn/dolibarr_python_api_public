import logging
import unittest

import config
from src.models.dolibarr.enums import Expired
from src.models.suppliers.bikable.product import BikableProduct

logging.basicConfig(level=config.loglevel)


class BikableProductTests(unittest.TestCase):
    def test_404(self):
        p = BikableProduct(
            url="https://bikable.se/reservdelar/kassetter/8-delad-kassett/shimano-8-speed-kassette-12-32-hg200-uden-aeske33"
        )
        with self.assertRaises(ImportError):
            p.update_and_import_if_missing()
            # assert p.expired == Expired.TRUE

    @staticmethod
    def test_200():
        p = BikableProduct(
            url="https://bikable.se/reservdelar/kassetter/8-delad-kassett/shimano-8-speed-kassette-12-32-hg200-uden-aeske"
        )
        p.scrape_product()
        assert p.expired == Expired.FALSE

    @staticmethod
    def test_image():
        p = BikableProduct(
            url="https://bikable.se/reservdelar/kassetter/8-delad-kassett/shimano-8-speed-kassette-12-32-hg200-uden-aeske"
        )
        p.scrape_product()
        assert (
            p.image_url
            == "https://images.bikable.se/r/s/Shimano_8_speed_kassette_12-32_HG200_1630063774.webp"
        )

    @staticmethod
    def test_name():
        p = BikableProduct(
            url="https://bikable.se/reservdelar/bakvaxel/mtbcitybike-bakvaxel/shimano-acera-rd-m3020-78-speedbakvaxel"
        )
        p.scrape_product()
        assert p.label == "Shimano Acera RD-M3020 7/8 SpeedBakväxel"

    @staticmethod
    def test_cost_price():
        p = BikableProduct(
            url="https://bikable.se/reservdelar/bakvaxel/mtbcitybike-bakvaxel/shimano-acera-rd-m3020-78-speedbakvaxel"
        )
        p.scrape_product()
        assert p.cost_price >= 199

    @staticmethod
    def test_description():
        p = BikableProduct(
            url="https://bikable.se/reservdelar/bakvaxel/mtbcitybike-bakvaxel/shimano-acera-rd-m3020-78-speedbakvaxel"
        )
        p.scrape_product()
        assert len(p.description.split()) >= 10

    # @staticmethod
    # def test_login():
    #     cg = Cykelgear()
    #     assert cg.logged_in is False
    #     cg.__login__()
    #     assert cg.logged_in is True
    #
    # @staticmethod
    # def test_parse_order_table():
    #     cg = Cykelgear()
    #     cg.__login__()
    #     cg.parse_order_table()
    #     assert len(cg.orders) > 0
