import logging
from pathlib import Path

import config
from config.enums import Database, DolibarrBaseUrl
from src.models.dolibarr import DolibarrApi
from src.models.dolibarr.enums import DolibarrColumn, DolibarrEndpoint
from src.models.exceptions import MissingInformationError
from src.models.suppliers.enums import SupportedSupplier

logger = logging.getLogger(__name__)


class MyDolibarrApi(DolibarrApi):
    """This models my specific Dolibarr instance.
    It enables chosing between the testing and production instance on the server
    It loads my token and has methods that are tailored to my needs"""

    token: str = ""
    database: Database = config.database_to_test_against

    @property
    def url(self) -> str:
        """This dynamically sets the base_url"""
        if self.database == Database.TESTING:
            return f"{DolibarrBaseUrl.TESTING.value}api/index.php/"
        else:
            # fallback to production
            return f"{DolibarrBaseUrl.PRODUCTION.value}api/index.php/"

    def __get_token__(self):
        # if self.database == Database.PRODUCTION:
        #     raise Exception("production database is disabled for now")
        if not self.token:
            token_path = Path(config.file_root) / "authentication" / self.database.value
            with open(token_path) as keyfile:
                self.token = str(keyfile.read()).strip()
                logger.debug(f"got token: {self.token}")

    def get_id_by_external_ref(
        self,
        codename: SupportedSupplier,
        external_ref: str,
        endpoint: DolibarrEndpoint,
        # column_to_search: DolibarrColumn = None,
    ) -> int:
        """This models getting an id from Dolibarr based on the external external_ref and codename"""
        self.__get_token__()
        from src.models.dolibarr.supplier import DolibarrSupplier

        dolibarr_supplier = DolibarrSupplier(codename=codename)
        if endpoint == DolibarrEndpoint.SUPPLIER_ORDER:
            column_to_search = DolibarrColumn.REF_SUPPLIER
        elif endpoint == DolibarrEndpoint.CUSTOMER_ORDER:
            column_to_search = DolibarrColumn.REF_CLIENT
        else:
            raise MissingInformationError(
                "did not get column to search and could not autodetect"
            )
        params = {
            "thirdparty_ids": dolibarr_supplier.id,
            "sqlfilters": f"(t.{column_to_search.value}:=:'{str(external_ref)}')",
        }
        response = self.call_list_api(endpoint=endpoint, params=params)
        if response.status_code == 200:
            # Return the id of the first object
            if response.json():
                return int(response.json()[0]["id"])
            else:
                return 0
                # if config.debug_responses:
                # raise ValueError(f"erroneous response from Dolibarr?:{response.text}")
        elif response.status_code == 404:
            # logger.debug(f"response from Dolibarr:{response.text}")
            return False
        else:
            raise ValueError(
                f"got {response.text} from the {endpoint.name} endpoint with params: {params}"
            )
