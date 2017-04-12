# -*- coding: utf-8 -*-
import socket
NORMAL = 0
ERROR = 1
TIMEOUT = 1


def ping_quick(ip, port, timeout=TIMEOUT):
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        address = (str(ip), int(port))
        cs.settimeout(timeout)
        cs.connect(address)
        return True
    except Exception, e:
        print "error:%s" % e
        return False
    finally:
        cs.close()


if __name__ == "__main__":
    print ping_quick("192.168.0.133", 10011, 5)
