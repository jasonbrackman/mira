# -*- coding: utf-8 -*-
import redis


def ping_redis(conn):
    try:
        conn.client_list()
        print "redis connect done."
        return True
    except redis.ConnectionError:
        print "redis connect failed."
        return False
