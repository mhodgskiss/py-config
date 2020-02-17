import argparse
import logging

import psycopg2
from psycopg2.extras import LoggingConnection
from klein_config import config

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="enable debug", action="store_true")


def params(**kwargs):
    """
    generate a dict of connection based on those provided by klein_config
    :param config: config imported from klein_config
    :param kwargs: expanded keyword arguments to build a connection with
    :return dict
    """
    p = dict()
    if config.has('postgres.username'):
        p["user"] = config.get('postgres.username')

    if config.has('postgres.password'):
        p["password"] = config.get('postgres.password')

    if config.has('postgres.database'):
        p["database"] = config.get('postgres.database')

    if config.has('postgres.host'):
        p["host"] = config.get('postgres.host', "127.0.0.1")

    if config.has('postgres.port'):
        p["port"] = config.get('postgres.port', "5432")

    for key, value in kwargs.items():
        p[key] = value

    return p


class PostgresConnection:

    def __init__(self):
        self.connection = None
        args, _ = parser.parse_known_args()
        self.debug = args

    def refresh(self, **kwargs):
        """
        refresh the connection
        :param config: dict of parameters to refresh the connection with (optional)
        :return psycopg.connection
        """
        if self.connection:
            self.connection.close()
        return self.connect(**kwargs)

    def connect(self, **kwargs):
        """
        connect to database
        :param config: dict of parameters to refresh the connection with (optional)
        :return psycopg.connection
        """

        if not kwargs:
            kwargs = {}

        p = params(**kwargs)

        if not p:
            return None

        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(__name__)
            p["connection_factory"] = LoggingConnection
            conn = psycopg2.connect(**p)
            conn.initialize(logger)
        else:
            conn = psycopg2.connect(**p)

        return conn


