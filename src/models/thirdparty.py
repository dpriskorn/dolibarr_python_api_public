import logging
from typing import Literal, Optional, Union

import config
from src.models.basemodels.my_base_model import MyBaseModel
from src.models.dolibarr.enums import DolibarrEndpoint
from src.models.marketplaces.sello.enums import SelloCountryCode

logger = logging.getLogger(__name__)


class Thirdparty(MyBaseModel):
    city: str = ""
    country_code: Optional[SelloCountryCode] = None
    email: str = ""
    family_name: Optional[str] = ""
    given_name: Optional[str] = ""
    id: Optional[str] = ""
    mobile: Optional[str] = ""
    tradera_alias: Optional[str] = ""
    address: Optional[str] = ""
    zip: Optional[str] = ""

    @property
    def name(self):
        return f"{self.given_name} {self.family_name}"

    @property
    def thirdparty_url(self):
        return f"{self._base_url}societe/card.php?socid={self.id}"

    def find_thirdparty_customer_id_by_tradera_alias_or_false(
        self,
    ) -> Union[int, Literal[False]]:
        # We search through every single customer
        if not self.tradera_alias:
            raise ValueError("tradera_alias was None")
        logger.info(f"Looking up if {self.tradera_alias} already exists")
        # We get all the thirdparties because the API does not
        # support searching for custom extrafields like "tradera_alias"
        r = self.api.call_list_api(
            DolibarrEndpoint.THIRDPARTIES,
            {"mode": 1, "sqlfilters": "(t.datec:>:'20200801')", "limit": 1000},
        )
        results = r.json()
        if config.debug_responses:
            logger.debug("response:")
            print(results)
        logger.info(f"Got {len(results)} thirdparties in total")
        # Find the right one
        for thirdparty in results:
            res = self.extrafield(thirdparty, "tradera_alias")
            # logger.debug(f"tradera_alias:{res}")
            if res and res.strip() == self.tradera_alias:
                # We found a match
                logger.debug("Match found!")
                return int(thirdparty["id"])
        # No match found
        logger.debug("No match found in Dolibarr")
        return False
