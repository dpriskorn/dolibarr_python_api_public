import logging

from requests import Session

import config
from src.controllers.supplier.login import SupplierLoginContr
from src.models.exceptions import LoginError
from src.models.suppliers.cycleservicenordic import CycleServiceNordic

logger = logging.getLogger(__name__)


class CsnLoginContr(SupplierLoginContr, CycleServiceNordic):
    def login(self) -> Session:
        logger.info(f"Logging in to {self.codename.name}")
        payload = self.__get_json_auth_data__("csn")
        logger.debug(payload)
        url = f"{self.base_url.value}en/login?json=true"
        # https://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
        # Use 'with' to ensure the session context is closed after use.
        session = Session()
        session.get(url)
        # http://stackoverflow.com/questions/46028156/ddg#46028242
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.cycleservicenordic.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://www.cycleservicenordic.com/se/login",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers",
        }

        params = (("redirect", "/se/login"),)
        r = session.post(url, data=payload, headers=headers, params=params)
        if config.write_test_data:
            with open("/tmp/test.html", "w") as f:
                f.write(r.text)
        if r.status_code == 200:
            data = r.json()
            if data["signincompleted"] is True:
                logger.info("Login success")
                self.session = session
                return session
            else:
                raise LoginError(f"Login failed. Got {r.text}")
        else:
            raise LoginError(
                f"Got {r.status_code} from {self.codename.name} when "
                + "trying to log in"
            )
