import os
from mock import mock
import argparse
import logging

host = os.environ.get('POSTGRES_HOST')
if host is None:
    host = 'localhost'

dummyConfig = {
    'POSTGRES_HOST': host,
    'POSTGRES_PORT': '5432', 
    'POSTGRES_DATABASE': 'test',
    'POSTGRES_USERNAME': 'postgres',
    'POSTGRES_PASSWORD': 'password'
}


@mock.patch.dict(os.environ, dummyConfig)
class TestPostgres(object):

    def test_params(self):
        from src.klein_postgres.connect import params
        p = params()
        assert p == dict(
            database="test", 
            user="postgres",
            password="password",
            host=host,
            port="5432"
        )  

    def test_params_with_custom_values(self):
        from src.klein_postgres.connect import params
        tmp_params = dict(
            database="tmp_db", 
            user="tmp_username",
            password="tmp_password",
            host="tmp_host",
            port="tmp_port"
        )
        p = params(**tmp_params)
        assert p == tmp_params

    def test_connect_with_no_params(self):
        from src.klein_postgres.postgres import connect
        connect()

    def test_connect_with_custom_params(self):
        from src.klein_postgres.postgres import connect
        connect(database="postgres")
        
    @mock.patch('argparse.ArgumentParser.parse_known_args',return_value=(argparse.Namespace(debug=True, config=None, common=None), argparse.Namespace()))
    def test_connect_with_logging_connection(self, args, caplog):
        caplog.set_level(logging.DEBUG)
        from src.klein_postgres.postgres import connect
        conn = connect()
        query = b"CREATE TABLE loggingTest (id serial primary key);"
        conn.cursor().execute(query)
        msg = caplog.records[0].msg
        assert (query == msg)