import logging
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup  # type: ignore
from requests import Session

from src.models.exceptions import MissingInformationError, ParseError
from src.models.supplier.product.sek_bike_product import SekBikeProduct
from src.models.suppliers.enums import SupplierBaseUrl, SupportedSupplier
from src.models.suppliers.hoj24.login import Hoj24Login

logger = logging.getLogger(__name__)


class Hoj24Product(SekBikeProduct):
    """SKUs from this supplier are numeric only with dashes"""

    codename: SupportedSupplier = SupportedSupplier.HOJ24
    base_url: SupplierBaseUrl = SupplierBaseUrl.HOJ24
    base_api_url: str = "https://api.hoj24.se/json/"
    session: Optional[Session] = None
    data: List[Dict[str, Any]] = list()
    base_image_url: str = "https://cdn1.gung.io/fit-in/1100x1100/filters:fill(white):background_color(white):format(jpeg)/"
    model_config = {"extra": "forbid", "arbitrary_types_allowed": "true"}

    def __login__(self):
        if not isinstance(self.session, Session):
            login = Hoj24Login()
            self.session = login.get_login_session()

    def __scrape_product__(self):
        """Hoj24 uses Gung PIM API which does not require logging in
        The refs are the same as before when they were called Jofrab"""
        logger.debug("__scrape_product__: Running")
        self.__login__()
        if not self.sku:
            if self.url:
                if "https://shop.hoj24.se" not in self.url:
                    raise ValueError("not a valid Hoj24 url")
                else:
                    """https://shop.hoj24.se/product/18-567-01"""
                    self.sku = self.url.split("/")[-1]
            else:
                raise ValueError("no ref or url provided")
        if not self.session:
            raise ValueError("self.session was None")
        self.__scrape_from_ref__()
        self.__parse_data__()
        self.scraped = True

    def __scrape_from_ref__(self):
        url = f"{self.base_api_url}products-list-with-flow-filter"
        # logger.debug(f"using url: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            # 'Accept-Encoding': 'gzip, deflate, br',
            # Already added when you pass json=
            # 'Content-Type': 'application/json',
            "Origin": "https://shop.hoj24.se",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://shop.hoj24.se/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }
        params = {
            "flow": "2",
        }
        json_data = [
            str(self.sku),
        ]
        r = self.session.post(url=url, json=json_data, headers=headers, params=params)
        if r.status_code == 200:
            self.data = r.json()
            # pprint(data)
            # exit()
        else:
            raise ValueError(f"Got {r.status_code} from Hoj24. {r.text}")

    def __parse_data__(self) -> None:
        """Parse the json data from the GUNG PIM API
        Se data/hoj24 för exempel på json"""
        if not self.data:
            raise MissingInformationError("no data")
        else:
            data = self.data[0]
            self.label = data["name"]
            # pprint(data)
            # exit()
            extra = data["extra"]

            ## GUNG ITEMS ##
            gung_items = extra["gungItems"]
            self.stock_quantity = int(gung_items["inventory"])
            self.net_weight = float(gung_items["netWeight"])
            self.cost_price = float(gung_items["unitPrice"])
            self.description = gung_items["description2"]

            ## PIM ##
            pim = extra["pim"]
            self.list_price = pim["rek-pris"]
            status = pim.get("ArticleStatus", None)
            if status is None:
                logger.warning("No ArticleStatus for this product")
            else:
                if status == "AKTIV":
                    self.available = True
                elif status == "NYHET":
                    self.available = True
                elif status == "UTGÅENDE":
                    input("Denna produkt är utgående (press enter to continue)")
                    self.scheduled_for_expiration = True
                    self.available = True
                else:
                    raise ParseError(f"status: {status} not supported yet, please fix")

            ## IMAGES ##
            images = extra["images"]
            # We only support the first image
            self.image_url = self.base_image_url + images[0]["s3Uri"]

    @property
    def generated_url(self) -> str:
        if not self.sku:
            raise MissingInformationError("no sku")
        # We hardcode here because using the enum did not work for some reason
        return f"https://shop.hoj24.se/product/{self.sku}"
