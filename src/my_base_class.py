import json
from typing import Any, Dict, List

import pytz
from pydantic import BaseModel

import config
from config import Database
from config.enums import DolibarrBaseUrl
from src.helpers.enums import FloatCleanType, StripType
from src.models.dolibarr.my_dolibarr_api import MyDolibarrApi


class MyBaseClass(BaseModel):
    api: MyDolibarrApi = MyDolibarrApi()  # default to production
    stockholm_timezone: Any = pytz.timezone("Europe/Stockholm")
    testing: bool = False

    class Config:
        arbitrary_types_allowed = True
        # extra = "forbid" # this causes massive test failure

    @property
    def _base_url(self) -> str:
        if self.api.database == Database.TESTING:
            return DolibarrBaseUrl.TESTING.value
        else:
            return DolibarrBaseUrl.PRODUCTION.value

    @staticmethod
    def convert_dolibarr_product_list_to_objects(
        data: List[Dict[Any, Any]]
    ) -> List[Any]:
        # convert JSON to product objects
        product_objects: List = []
        from src.models.dolibarr.product import DolibarrProduct

        for product in data:
            p = DolibarrProduct(**product)
            product_objects.append(p)
        if len(product_objects) > 0:
            return product_objects
        else:
            raise ValueError(
                "Could not find any products in the response from dolibarr"
            )

    @staticmethod
    def price_cleanup(price_stripping_type: StripType, price: str) -> str:
        if price_stripping_type == StripType.KR_BEFORE:
            # used for shimano
            return price.replace("kr ", "").replace("\xa0", "").replace(",", ".")
        elif price_stripping_type == StripType.KR_AFTER:
            return price.replace(" kr", "").replace(" ", "").replace(",", ".")
        elif price_stripping_type == StripType.COLON_DASH:
            # used for jaguarverken
            return price.replace(":-", "").replace(",", ".").replace(" ", "")
        elif price_stripping_type == StripType.EUR_AFTER:
            return price.replace("EUR", "").replace("\xa0", "").replace(",", ".")
        else:
            raise ValueError("Could not parse price stripping type.")

    @staticmethod
    def response_to_int_or_fail(symbol):
        try:
            return int(symbol.replace('"', ""))
        except ValueError as err:
            raise ValueError(
                "Could not convert Dolibarr response: '{symbol}' i" + "to an integer."
            ) from err

    @staticmethod
    def extrafield(data: dict[Any, Any], field: str) -> str:
        """Get extrafield as string or return None"""
        # workaround bug? in the API where this is an empty list for
        # some reason
        # TDOO retire this in favor of OOP property methods
        if isinstance(data, dict) and data.get("array_options"):
            return str(data["array_options"]["options_" + field])
        else:
            return ""

    @staticmethod
    def empty_or_false(symbol) -> bool:
        if not symbol or symbol == "" or symbol == "0":
            return True
        else:
            return False

    @staticmethod
    def clean_number_to_float(value, clean_type: FloatCleanType = None):
        if not value or value == "0" or value == 0:
            return 0
        if clean_type:
            if clean_type == FloatCleanType.SCANDINAVIAN:
                # Support "1.799,00"
                return float(value.replace(".", "").replace(",", "."))
            if clean_type == FloatCleanType.AMERICAN:
                # Support "1,799.00 from e.g. CSN"
                return float(value.replace(",", ""))

    @staticmethod
    def __get_json_auth_data__(filename) -> Dict[Any, Any]:
        """This method gets secret data from file when needed to log in"""
        with open(f"{config.file_root}authentication/" + filename + ".json") as keyfile:
            return json.loads(keyfile.read())
