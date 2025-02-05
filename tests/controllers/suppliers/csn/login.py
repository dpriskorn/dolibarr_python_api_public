from unittest import TestCase

from requests import Session

from src.controllers.suppliers.csn.login import CsnLoginContr


class CycleServiceNordicTests(TestCase):
    @staticmethod
    def test_login():
        session = CsnLoginContr().login()
        assert isinstance(session, Session) is not None
