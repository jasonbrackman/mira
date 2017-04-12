# -*- coding: utf-8 -*-
import socket


def send_command(host, port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(command)
    # while 1:
    #     result = sock.recv(2048)
    #     if result:
    #         print result
    result = sock.recv(2048)
    print result
    sock.close()


if __name__ == "__main__":
    send_command("192.168.0.133", 10011, "tskill maya")
