# -*- coding: utf-8 -*-
import redis
from . import get_conf_data


def get_redis_conn():
    conf_data = get_conf_data.get_conf_data("server")
    server = conf_data["redis_server"]
    port = conf_data["redis_port"]
    conn = redis.Redis(host=server, port=port)
    return conn
