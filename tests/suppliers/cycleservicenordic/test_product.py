import logging
from unittest import TestCase

from bs4 import BeautifulSoup

import config
from src.models.suppliers.cycleservicenordic.product import CycleServiceNordicProduct

logging.basicConfig(level=config.loglevel)


class CycleServiceNordicProductTests(TestCase):
    @staticmethod
    def test__extract_json_ld_data__():
        html = """
        <script type="application/ld+json" nonce="2HyjmfGw3hfwJNmsxfEoYxKiyO80xFqjktdLml5WIEQ=">
    {
  "@context": "https://schema.org",
  "@type": "Product",
  "productID": "2503250000",
  "name": "XLC Mirror MR-K10",
  "image": "https://resources.chainbox.io/5/cycleservicenordic/public/pim/145cba5c-c6d5-4f1f-bef4-d5a456bd70fd/2503250000_default.jpg",
  "sku": "2503250000",
  "offers": {
    "@type": "Offer",
    "availability": "http://schema.org/OutOfStock"
  }
}
  </script>"""
        soup = BeautifulSoup(html, features="lxml")
        p = CycleServiceNordicProduct(
            url="https://www.cycleservicenordic.com/en/mirrors/xlc-mr-k10"
        )
        p.__extract_json_ld_data__(soup=soup)
        assert (
            p.image_url
            == "https://resources.chainbox.io/5/cycleservicenordic/public/pim/145cba5c-c6d5-4f1f-bef4-d5a456bd70fd/2503250000_default.jpg"
        )
        assert p.available is False
        assert p.sku == "2503250000"

    @staticmethod
    def test_valid_url():
        p = CycleServiceNordicProduct(
            url="https://www.cycleservicenordic.com/en/mirrors/xlc-mr-k10"
        )
        p.scrape_product()
        assert p.label == "XLC Mirror MR-K10"
        assert p.ean == "4055149339630"
        assert (
            p.image_url
            == "https://resources.chainbox.io/5/cycleservicenordic/public/pim/145cba5c-c6d5-4f1f-bef4-d5a456bd70fd/2503250000_default.jpg"
        )
        # assert p.available is True
        assert p.sku == "2503250000"
        assert p.cost_price == 101.67
        assert p.list_price == 229.00
        assert p.description == (
            "Item type: Mirror\n"
            "Brand: XLC\n"
            "Item name: MR-K10\n"
            "Description: Left side, aluminium clamp, nylon casing, nylon rod, "
            "break-proof stainless steel mirror glass, 3D adjustable, 180° angle, 360° "
            "rotatable\n"
            "Mounting: Bar clamp mount (outer Ø21-26 mm)\n"
            "Package: '1/1"
        )

    def test_invalid_url(self):
        p = CycleServiceNordicProduct(
            url="https://www.3cycleservicenordic.com/en/mirrors/xlc-mr-k10"
        )
        with self.assertRaises(ValueError):
            p.scrape_product()

    @staticmethod
    def test_valid_url2():
        p = CycleServiceNordicProduct(
            url="https://www.cycleservicenordic.com/en/hjul-root_whe10/connect-wheel-700c-700c-rear-943054"
        )
        p.scrape_product()
        assert p.label == "CONNECT Wheel 700c 700c Rear"
        assert p.ean == "5708280021825"
        assert (
            p.image_url
            == "https://resources.chainbox.io/5/cycleservicenordic/public/pim/2e4ab3d2-ea8b-4181-aeac-11db8009c871/943054_default.jpg"
        )
        assert p.available is True
        assert p.sku == "943054"
        assert p.cost_price == 640.91
        assert p.list_price == 1499.0
        assert p.brand == "CONNECT"

    @staticmethod
    def test_available():
        p = CycleServiceNordicProduct(
            url="https://www.cycleservicenordic.com/en/hjul-root_whe10/connect-wheel-700c-700c-front-945021"
        )
        p.scrape_product()
        assert p.available is True

    @staticmethod
    def test_sku_scrape():
        p = CycleServiceNordicProduct(sku="593 5680")
        p.scrape_product()
        assert p.available is True
