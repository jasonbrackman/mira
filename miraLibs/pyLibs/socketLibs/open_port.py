# -*- coding: utf-8 -*-
import socket
import subprocess
import sys
import add_rule
import miraLibs.osLibs.get_local_ip
import ping


def open_port(port, host=None):
    if host is None:
        host = miraLibs.osLibs.get_local_ip.get_local_ip()
    add_rule.add_rule("mira", port)
    status = ping.ping(host, port, 0.1)
    if status:
        print "%s %s is in using" % (host, port)
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    while True:
        try:
            conn, addr = sock.accept()
            command = conn.recv(2048)
            if command:
                try:
                    conn.send("%s get command: %s\n" % (host, command))
                    subprocess.Popen(command, shell=True)
                    conn.send("%s run [%s] successful.\n" % (host, command))
                except:
                    conn.send("%s run %s failed.\n" % (host, command))
        except KeyboardInterrupt:
            print "exit"
            sys.exit(0)
