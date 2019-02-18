import json
import os
import pytest
from mock import mock

dummyConfig = {
    'POSTGRES_HOST': '127.0.0.1', 
    'POSTGRES_PORT': '5432', 
    'POSTGRES_DATABASE': 'test',
    'POSTGRES_USERNAME': 'postgres',
    'POSTGRES_PASSWORD': 'password'

    }


@mock.patch.dict(os.environ, dummyConfig)
class TestPostgres(object):

    def test_params(self):
        from src.klein_postgres.postgres import params
        p = params()
        assert p == dict(
            database="test", 
            user="postgres",
            password="password",
            host="127.0.0.1",
            port="5432"
        )  

    def test_params_with_custom_values(self):
        from src.klein_postgres.postgres import params
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
        
        
