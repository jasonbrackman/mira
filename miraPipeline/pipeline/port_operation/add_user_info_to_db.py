# -*- coding: utf-8 -*-
import getpass
import redis
from miraLibs.osLibs import get_local_ip, get_mac_address
from miraLibs.redisLibs import user_settings, get_redis_connection


def add_user_info_to_db():
    conn = get_redis_connection.get_redis_connection()
    try:
        conn.client_list()
    except redis.ConnectionError:
        print "redis connect failed."
        return
    user = getpass.getuser()
    ip = get_local_ip.get_local_ip()
    mac = get_mac_address.get_mac_address(ip)
    user_settings.add_user(conn, user, ip=ip, mac=mac)


if __name__ == "__main__":
    add_user_info_to_db()

