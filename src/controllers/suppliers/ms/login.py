import logging

from bs4 import BeautifulSoup, SoupStrainer
from requests import Response, Session

import config
from src.controllers.supplier.login import SupplierLoginContr
from src.models.exceptions import LoginError
from src.models.suppliers.messingschlager import Messingschlager

logger = logging.getLogger(__name__)


class MsLoginContr(SupplierLoginContr, Messingschlager):
    """We need Messingschlager to get the supplier specific attributes"""

    def login(self) -> Session:
        """This logs in to Messingschlager and stores the session in self.session"""
        logger.info("Logging in to MS")
        payload = self.__get_json_auth_data__("messingschlager")
        url = f"{self.base_url.value}en/login"
        logger.debug(f"using URL: {url}")
        # https://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module
        # Use 'with' to ensure the session context is closed after use.
        with Session() as session:
            r = session.get(url)
            # http://stackoverflow.com/questions/46028156/ddg#46028242
            soup = BeautifulSoup(r.text, features="lxml")
            token = soup.find("input", {"name": "csrf_token"})["value"]
            # print(token)
            payload["csrf_token"] = token
            # print(r.request.headers)
            # print(r.status_code)
            # print(r.headers)
            r = session.post(
                "https://www.messingschlager.com/",
                data=payload,
                headers={
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            # print(r.request.body)
            # print(r.request.headers)
            # # print(r.request.data)
            # print(r.status_code)
            # print(r.headers)
            if config.write_test_data:
                with open("/tmp/test.html", "w") as f:
                    f.write(r.text)
                    # raise DebugExit()
            # We get 302 when succesfully logged in
            if r.status_code in [302, 200]:
                if self.cart_link_is_present(response=r):
                    logger.info("Login successful")
                    # self.session = session
                    self.success = True
                    return session
                else:
                    raise LoginError("could not find cart link")
            else:
                raise ValueError(f"Got {r.status_code} from MS")

    @classmethod
    def cart_link_is_present(cls, response: Response) -> bool:
        # Define a SoupStrainer to parse only <a> tags
        only_a_tags = SoupStrainer("a")

        # Parse the HTML content using the SoupStrainer
        soup = BeautifulSoup(response.text, "lxml", parse_only=only_a_tags)

        # Find the <a> tag
        cart_link = soup.find("a", title="Cart")

        if cart_link is not None:
            return True
        return False
