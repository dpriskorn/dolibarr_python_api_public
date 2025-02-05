import logging
import unittest

import config
from src.models.exceptions import (
    MissingInformationError,
    ProductNotFoundError,
)
from src.models.suppliers.shimano.login import ShimanoLogin
from src.models.suppliers.shimano.product import ShimanoProduct

logging.basicConfig(level=config.loglevel)


logger = logging.getLogger(__name__)


class ShimanoProductTests(unittest.TestCase):
    """Tests for the ShimanoProduct class"""

    session = ShimanoLogin().login_and_get_session()

    def test_scrape_with_invalid_ref(self):
        p = ShimanoProduct(sku="testESG3C41A2775DX", session=self.session)
        with self.assertRaises(ProductNotFoundError):
            p.scrape_product()

    def test_instantiation_with_no_arguments(self):
        with self.assertRaises(MissingInformationError):
            p = ShimanoProduct(session=self.session)
            p.scrape_product()

    def test_instantiation_with_empty_url(self):
        with self.assertRaises(MissingInformationError):
            p = ShimanoProduct(url="", session=self.session)
            p.scrape_product()

    def test_instantiation_with_invalid_url(self):
        with self.assertRaises(ValueError):
            p = ShimanoProduct(url=1234, session=self.session)  # type: ignore
            p.scrape_product()

    def test_instantiation_with_wrong_url(self):
        with self.assertRaises(ValueError):
            p = ShimanoProduct(
                url="https://www.cykelgear.se/reservdelar/bakvaxel/vaxelora/vaxelora-type-x",
                session=self.session,
            )
            p.scrape_product()

    def test_scraping_with_valid_url(self):
        p = ShimanoProduct(
            url="https://b2b.shimano.com/bike/se/sv/product/PT101081",
            session=self.session,
        )
        p.scrape_product()
        self.assertEqual(p.sku, "PT101081")
        print(p)
        assert p.label == "Gängtapp TAP-10 10mm"
        assert p.cost_price >= 100
        assert p.scraped is True
        assert p.stock_quantity > 0
        assert p.available is True

    def test__extract_ref_from_url__(self):
        p = ShimanoProduct(
            url="https://b2b.shimano.com/bike/se/sv/product/PT101081",
            session=self.session,
        )
        p.__extract_ref_from_url__()
        assert p.sku == "PT101081"
