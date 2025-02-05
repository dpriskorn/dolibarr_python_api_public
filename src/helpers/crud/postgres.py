import logging
from typing import Any

import paramiko
import psycopg2  # type: ignore
import sshtunnel
from sshtunnel import SSHTunnelForwarder

import config
from config.enums import DatabaseUser
from src.models.dolibarr.my_dolibarr_api import MyDolibarrApi

logger = logging.getLogger(__name__)


class Postgres(MyDolibarrApi):
    database_user: DatabaseUser = DatabaseUser.DOLIBARR
    connection: Any | None = None  # typing: connection
    model_config = {"arbitrary_types_allowed": "true"}

    def __del__(self):
        """Deconstructor that disconnect from the database"""
        self.disconnect()

    def connect(self):
        """Connect if we don't already have a connection"""
        if self.connection is None:
            if config.use_ssh_tunnel:
                try:
                    mypkey = paramiko.Ed25519Key.from_private_key_file(
                        "/home/dpriskorn/.ssh/ovh"
                    )
                    sshtunnel.SSH_TIMEOUT = 5.0
                    sshtunnel.TUNNEL_TIMEOUT = 5.0
                    tunnel = SSHTunnelForwarder(
                        (config.ssh_host_ip, 22),
                        ssh_username=config.ssh_username,
                        ssh_pkey=mypkey,
                        remote_bind_address=("localhost", config.postgresql_port),
                    )

                    tunnel.start()
                    return psycopg2.connect(
                        database=self.database.value,
                        user=self.database_user.value,
                        host="127.0.0.1",
                        port=tunnel.local_bind_port,
                    )
                except ConnectionError:
                    print("Unable to connect to the database")
            else:
                with open(
                    config.file_root + "authentication/postgres/" + self.database.value
                ) as file:
                    password = file.read().strip()
                    logger.debug(f"got password: {password}")
                try:
                    self.connection = psycopg2.connect(
                        host=config.postgresql_host,
                        port=config.postgresql_port,
                        database=self.database.value,
                        user=self.database_user.value,
                        password=password,
                    )
                    logger.info(f"Connected to {self.database.name} database")
                except ConnectionError:
                    print("Unable to connect to the database")

    def disconnect(self):
        if self.connection is not None:
            try:
                self.connection.close()
                self.connection = None
            except (ConnectionError, TypeError):
                print("unable to disconnect from db")
