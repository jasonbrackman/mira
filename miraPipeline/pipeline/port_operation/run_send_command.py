# -*- coding: utf-8 -*-
import threading
import redis
from miraLibs.pyLibs import ConfParser
from miraLibs.pyLibs.socketLibs import send_command
from miraLibs.redisLibs import user_settings, get_redis_connection


def run_send_command(command, only=[], exclude=[]):
    cp = ConfParser.ConfParser(__file__)
    port = cp.conf_data.get("port")
    conn = get_redis_connection.get_redis_connection()
    try:
        conn.client_list()
        print "redis connect done."
    except redis.ConnectionError:
        print "redis connect failed."
        return
    user_info = user_settings.get_user_info(conn, ["name", "ip"])
    for user in user_info:
        if only:
            if user["name"] in only:
                send_user_command(user, port, command)
        else:
            if user["name"] in exclude:
                continue
            send_user_command(user, port, command)


def send_user_command(user, port, command):
    try:
        t = threading.Thread(target=send_command.send_command, args=(user["ip"], port, command))
        t.start()
        message_str = "send command {:<5}{:<%s}{:<16}{ip}" % (len(command)+5)
        print message_str.format("", command, user["name"], ip=user["ip"])
    except IOError as e:
        print "Can't connect to {:<5}{:<16}{ip}".format("", user["name"], ip=user["ip"])
        print str(e)


if __name__ == "__main__":
    command = "\"C:/Program Files/Thinkbox/Deadline7/bin/deadlinelauncher.exe\""
    run_send_command(command)
    command = "\"C:/Program Files/Thinkbox/Deadline7/bin/deadlineslave.exe\""
    run_send_command(command)
