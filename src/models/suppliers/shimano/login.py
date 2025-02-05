import logging

import requests
from bs4 import BeautifulSoup  # type: ignore

from src.helpers.console import console
from src.models.basemodels.my_base_model import MyBaseModel
from src.models.exceptions import LoginError
from src.models.suppliers.enums import SupplierBaseUrl

logger = logging.getLogger(__name__)


class ShimanoLogin(MyBaseModel):
    base_url: SupplierBaseUrl = SupplierBaseUrl.SHIMANO

    @classmethod
    def login_and_get_session(cls) -> requests.Session:
        """Logs in and returns a session object"""
        token_login_url = (
            "https://api.c5vp9gk-shimanoin2-p1-public."
            "model-t.cc.commerce.ondemand.com/"
            "authorizationserver/oauth/token"
        )
        with console.status("Logging in"):
            session = requests.Session()
            response = session.post(
                token_login_url,
                data=MyBaseModel().__get_json_auth_data__(filename="shimano"),
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;"
                    + "q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "DNT": "1",
                    "Host": "api.c5vp9gk-shimanoin2-p1-public.model-t.cc.commerce.ondemand.com",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "cross-site",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; "
                    + "rv:83.0) Gecko/20100101 Firefox/83.0",
                },
            )
            if response.status_code == 200:
                logger.info("Login ok")
                # Extract token from response and add it to the session headers
                data = response.json()
                """{
                  "access_token" : "Df-w1_mrB61wUt5POQiraHOchUE",
                  "token_type" : "bearer",
                  "refresh_token" : "q5WEOpt5pQta5aSpWKEQizXPlI8",
                  "expires_in" : 35697,
                  "scope" : "basic openid"
                }"""
                token = data["access_token"]
                token_type = data["token_type"]
                session.headers["Authorization"] = f"{token_type} {token}"
                session.headers["User-Agent"] = (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; "
                    + "rv:83.0) Gecko/20100101 Firefox/83.0"
                )
                session.headers["Host"] = (
                    "api.c5vp9gk-shimanoin2-p1-public.model-t.cc."
                    "commerce.ondemand.com"
                )
                session.headers["Accept"] = "application/json"
                session.headers["Origin"] = "https://b2b.shimano.com"
                session.headers["Referer"] = "https://b2b.shimano.com/"
                session.headers["Sec-Fetch-Dest"] = "empty"
                session.headers["Sec-Fetch-Mode"] = "cors"
                session.headers["Sec-Fetch-Site"] = "cross-site"
                session.headers["DNT"] = "1"
                return session
            elif response.status_code == 401:
                raise LoginError("Got 401 unauthorized from Shimano")
            else:
                raise LoginError(f"Got {response.status_code} from Shimano")
