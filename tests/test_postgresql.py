import logging

import config
from src.helpers.crud.postgres import Postgres

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)


class TestPostgres:
    def test_db_connect(self):
        # p = Postgres(database=Database.TESTING)
        p = Postgres()
        p.connect()
        assert p.connection is not None

    def test_db_connect_close(self):
        # p = Postgres(database=Database.TESTING)
        p = Postgres()
        p.connect()
        assert p.connection is not None
        p.disconnect()
        assert p.connection is None
