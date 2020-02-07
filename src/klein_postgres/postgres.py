# -*- coding: utf-8 -*-
import psycopg2.extras

from .connect import PostgresConnection

connection_object = PostgresConnection()
connect = connection_object.connect
connection = connection_object.connect()
refresh = connection_object.refresh()
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) if connection else None