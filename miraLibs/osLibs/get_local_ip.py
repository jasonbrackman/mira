# -*- coding: utf-8 -*-
import socket


def get_local_ip():
    local_ip = socket.gethostbyname(socket.gethostname())
    return local_ip


if __name__ == "__main__":
    print get_local_ip()
