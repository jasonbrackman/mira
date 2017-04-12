# -*- coding: utf-8 -*-
import connect_redis
from miraLibs.pyLibs import ConfParser


def get_redis_connection():
    conf_data = ConfParser.ConfParser(__file__)
    host = conf_data.conf_data.get("redis_server")
    port = conf_data.conf_data.get("redis_port")
    conn = connect_redis.connect_redis(host, port)
    return conn
