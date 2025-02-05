import logging
from unittest import TestCase

import config
from src.models.suppliers.hoj24.login import Hoj24Login

logging.basicConfig(level=config.loglevel)


class JofrabLoginTests(TestCase):
    """Tests for the JofrabProduct class"""

    @staticmethod
    def test_login():
        login = Hoj24Login()
        s = login.get_login_session()
        # print(s.cookies.get_dict())
        # make sure we get a cookie back
        assert s.cookies.get_dict()["JSESSIONID"] != ""
