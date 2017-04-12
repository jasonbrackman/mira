# -*- coding: utf-8 -*-
import socket
NORMAL = 0
ERROR = 1
TIMEOUT = 1


def ping(ip, port, timeout=TIMEOUT):
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        address = (str(ip), int(port))
        status = cs.connect_ex(address)
        cs.settimeout(timeout)
        # this status is return back from tcp server
        if status == NORMAL:
            return True
        else:
            return False
    except Exception, e:
        print "error:%s" % e
        return False
    finally:
        cs.close()


if __name__ == "__main__":
    print ping("192.168.0.133", 10011, 5)
