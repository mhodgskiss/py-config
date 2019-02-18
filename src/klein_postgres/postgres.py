# -*- coding: utf-8 -*-
from klein_config import config
import psycopg2

def params(**kwargs):
    '''
    generate a dict of connection based on those provided by klein_config
    :param kwargs: expanded keyword arguments to build a connection with
    :return dict 
    '''
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

    for key, value in kwargs:
        p[key] = value

    return p

def refresh(conn_conf = None):
    '''
    refresh the connection
    :param config: dict of parameters to refresh the connection with (optional)
    :return psycopg.connection
    '''
    if connection: 
        connection.close()
    connect(conn_conf)

def connect(conn_conf= None):
    '''
    connect to database
    :param config: dict of parameters to refresh the connection with (optional)
    :return psycopg.connection
    '''
    return psycopg2.connect(params(**conn_conf))
    
connection_params = params()
connection = connect()
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)