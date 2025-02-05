import logging
from typing import Optional

from requests import Session

from src.models.basemodels.my_base_model import MyBaseModel
from src.models.suppliers.enums import SupplierBaseUrl

logger = logging.getLogger(__name__)


class Hoj24Login(MyBaseModel):
    base_url: SupplierBaseUrl = SupplierBaseUrl.HOJ24
    session: Optional[Session] = None

    class Config:  # dead: disable
        arbitrary_types_allowed = True

    def get_login_session(self) -> Session:
        """This function logs into Hoj24 and returns a session"""
        if not isinstance(self.session, Session):
            logger.info("Logging in to Hoj24")
            payload = self.__get_json_auth_data__(filename="hoj24")
            url = "https://api.hoj24.se/login"
            # https://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
            # Use 'with' to ensure the session context is closed after use.
            session = Session()
            session.get(url)
            r = session.post(
                url,
                data=payload,
                headers={
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            # with open("/tmp/test.html", "w") as f:
            #     f.write(r.text)
            if r.status_code == 200:
                logger.info("Login OK")
                self.session = session
                return session
            else:
                raise ConnectionError(
                    f"Got {r.status_code} from se when trying to log in"
                )
        else:
            logger.info("Returning existing session")
            return self.session
