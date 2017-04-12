# -*- coding: utf-8 -*-
import redis


def connect_redis(host, port):
    conn = redis.Redis(host, port)
    return conn
