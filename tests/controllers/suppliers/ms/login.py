from unittest import TestCase

from requests import Session

from src.controllers.suppliers.ms.login import MsLoginContr


class TestMsLoginContr(TestCase):
    def test_login(self):
        contr = MsLoginContr()
        session = contr.login()
        assert contr.success is True
        assert isinstance(session, Session)
