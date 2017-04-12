# -*- coding: utf-8 -*-
import redis
import time


def init_next_user_id(conn):
    conn.setnx("next_user_id", 0)


def add_user(conn, name, **kwargs):
    init_next_user_id(conn)
    pipe = conn.pipeline()
    end = time.time() + 5
    while time.time() < end:
        try:
            pipe.watch("next_user_id")
            user_id = int(pipe.get("next_user_id"))
            is_exist = pipe.setnx("user:%s:id" % name, user_id)
            if not is_exist:
                return
            pipe.multi()
            pipe.setnx("user:%s:name" % user_id, name)
            if kwargs:
                for key in kwargs:
                    pipe.setnx("user:%s:%s" % (user_id, key), kwargs[key])
            pipe.incr("next_user_id")
            pipe.execute()
            print "%s create successful." % name
            return
        except redis.exceptions.WatchError:
            pass


def get_id_by_user(conn, user_name):
    user_id = conn.get("user:%s:id" % user_name)
    return user_id


def add_user_filed(conn, name, **kwargs):
    if not kwargs:
        return
    user_id = get_id_by_user(conn, name)
    if user_id is None:
        add_user(conn, name)
    for key in kwargs:
        conn.set("user:%s:%s" % (user_id, key), kwargs[key])


def get_user_info(conn, fields):
    if isinstance(fields, basestring):
        fields = [fields]
    if not isinstance(fields, list):
        raise ValueError("fields must type of list.")
    data_list = list()
    all_id_keys = conn.keys("user:*:id")
    if not all_id_keys:
        return
    for id_key in all_id_keys:
        user_id = conn.get(id_key)
        temp_dict = dict()
        for field in fields:
            field_value = conn.get("user:%s:%s" % (user_id, field))
            temp_dict[field] = field_value
        data_list.append(temp_dict)
    return data_list


if __name__ == "__main__":
    conn = redis.Redis(host="127.0.0.1", port=6379)
    add_user(conn, "heshuai")
