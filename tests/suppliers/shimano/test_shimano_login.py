from unittest import TestCase

from requests import Session

from src.models.suppliers.shimano.login import ShimanoLogin


class TestShimanoLogin(TestCase):
    def test_login(self):
        session = ShimanoLogin().login_and_get_session()
        assert isinstance(session, Session)
        assert "Authorization" in dict(session.headers)
        assert len(dict(session.headers)["Authorization"]) == 34
