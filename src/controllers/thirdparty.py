import logging

from src.controllers.my_base_contr import MyBaseContr
from src.models.dolibarr import DolibarrEndpoint
from src.models.dolibarr.enums import DolibarrTable
from src.models.marketplaces.sello.enums import SelloCountryCode
from src.models.thirdparty import Thirdparty

logger = logging.getLogger(__name__)


class ThirdpartyContr(MyBaseContr, Thirdparty):
    def import_thirdparty(self) -> int:
        # TODO get name from attribute instead
        if (
            self.address,
            self.name,
        ) is None:
            raise ValueError("did not get what we needed")
        if self.country_code == SelloCountryCode.SWEDEN:
            country = "Sweden"
        elif self.country_code == SelloCountryCode.DENMARK:
            country = "Denmark"
        else:
            raise ValueError(f"Does not support country code {self.country_code}")
        data = {
            "client": "1",  # customer
            "code_client": "auto",
            "name": self.name,
            "name_alias": self.tradera_alias,
            "address": self.address,  # (order["address"] + " " + order["customer_address_2"]),
            "zip": self.zip,
            "town": self.city,
            "email": self.email,
            "phone": self.mobile,
            "country": country,
        }
        r = self.api.call_create_api(
            endpoint=DolibarrEndpoint.THIRDPARTIES, params=data
        )
        if r.status_code == 200:
            thirdparty_id = int(r.text.strip().replace('"', ""))
            logger.debug(f"thirdparty_id: '{thirdparty_id}'")
            thirdparty = Thirdparty(id=str(thirdparty_id))
            logger.info(f"Third party created: {thirdparty.thirdparty_url}")
        else:
            raise ValueError("Failed to create third party.")
        # insert extrafield - this is redundant but its more stable than the
        # name_alias because I don't know if I want to use that for anything
        # else down the road.
        self.create.insert_extrafield(
            DolibarrTable.THIRDPARTY, thirdparty_id, "tradera_alias", self.tradera_alias
        )
        # Set has address to true
        self.create.insert_extrafield(
            DolibarrTable.THIRDPARTY, thirdparty_id, "has_address", 1
        )
        return thirdparty_id
