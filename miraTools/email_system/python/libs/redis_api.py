# -*- coding: utf-8 -*-
import getpass
import redis
import time


class Email(object):
    def __init__(self):
        self.email_id = None
        self.title = None
        self.isRead = None
        self.content = None
        self.send_time = None
        self.sender = None
        self.acceptors = None


def init_next_user_id(conn):
    conn.setnx("next_user_id", 0)


def init_next_email_id(conn):
    conn.setnx("next_email_id", 0)


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
        print "user: %s is not created." % name
    for key in kwargs:
        conn.set("user:%s:%s" % (user_id, key), kwargs[key])


def add_email_field(conn, email_id, **kwargs):
    for key in kwargs:
        conn.set("email:%s:%s" % (email_id, key), kwargs[key])
    print "create email %s done" % email_id


def send_email(conn, sender_name, acceptor_list, **kwargs):
    sender_id = get_id_by_user(conn, sender_name)
    if sender_id is None:
        print "%s not initialize in the database" % sender_name
        return
    init_next_email_id(conn)
    pipe = conn.pipeline()
    end = time.time() + 5
    while time.time() < end:
        try:
            pipe.watch("next_email_id")
            email_id = int(pipe.get("next_email_id"))
            pipe.multi()
            # create email
            email_field_dict = dict()
            for acceptor in acceptor_list:
                email_field_dict["isReadBy%s" % acceptor] = 0
            add_email_field(pipe, email_id, **email_field_dict)
            add_email_field(pipe, email_id, **kwargs)
            pipe.incr("next_email_id")
            # add to sender sendBox
            pipe.lpush("user:%s:sendBox" % sender_id, email_id)
            pipe.ltrim("user:%s:sendBox" % sender_id, 0, 99)
            # add to acceptor box
            for acceptor in acceptor_list:
                acceptor_id = get_id_by_user(conn, acceptor)
                if acceptor_id is None:
                    print "%s is not initialize in the database" % acceptor
                    continue
                pipe.lpush("user:%s:receiveBox" % acceptor_id, email_id)
                pipe.ltrim("user:%s:receiveBox" % acceptor_id, 0, 99)
            pipe.execute()
            print "send email successful"
            return
        except redis.exceptions.WatchError:
            pass


def delete_email(conn, user_name, email_id_list, delete_from="sendBox"):
    user_id = get_id_by_user(conn, user_name)
    if user_id is None:
        print "%s is not initialize in the database." % user_name
        return
    user_box = conn.lrange("user:%s:%s" % (user_id, delete_from), 0, -1)
    email_id_list = [str(email_id) for email_id in email_id_list]
    pipe = conn.pipeline()
    pipe.multi()
    for email_id in email_id_list:
        if email_id not in user_box:
            continue
        pipe.lrem("user:%s:%s" % (user_id, delete_from), email_id, 0)
        if delete_from != "recycleBox":
            pipe.lpush("user:%s:recycleBox" % user_id, email_id)
            pipe.ltrim("user:%s:recycleBox" % user_id, 0, 99)
    pipe.execute()
    print "remove email done."


def get_receive_emails(conn, user_name, box="receiveBox"):
    user_id = get_id_by_user(conn, user_name)
    email_ids = conn.lrange("user:%s:%s" % (user_id, box), 0, -1)
    if not email_ids:
        return
    emails = list()
    for email_id in email_ids:
        title = conn.get("email:%s:title" % email_id)
        isRead = conn.get("email:%s:isReadBy%s" % (email_id, user_name))
        content = conn.get("email:%s:content" % email_id)
        send_time = conn.get("email:%s:send_time" % email_id)
        sender = conn.get("email:%s:sender" % email_id)
        acceptors = conn.get("email:%s:acceptors" % email_id)
        email = Email()
        email.email_id = email_id
        email.title = title
        email.isRead = isRead
        email.content = content
        email.send_time = send_time
        email.sender = sender
        email.acceptors = acceptors
        emails.append(email)
    return emails


def get_unread_emails(conn, user_name=getpass.getuser()):
    receive_emails = get_receive_emails(conn, user_name)
    if not receive_emails:
        return
    unread_emails = list()
    for email in receive_emails:
        is_read = int(email.isRead)
        if not is_read:
            unread_emails.append(email)
    return unread_emails


if __name__ == "__main__":
    conn = redis.Redis(host="127.0.0.1", port=6379)
    add_user(conn, "heshuai")
    add_user(conn, "zhaopeng")
    add_user(conn, "xiedonghang")
    # add_user(conn, "Administrator")
    # send_email(conn, "Administrator", ["heshuai"], title="test1", isRead=0, content="test1 content",
    #            sender="Administrator", acceptors=["heshuai"])
    # delete_email(conn, "heshuai", [0, 1, 2, 3], "receiveBox")
    # print get_receive_emails(conn, "heshuai")
