# -*- coding: utf-8 -*-
import os


def add_rule(name, port):
    delete_port_cmd = "netsh advfirewall firewall delete rule name=\"%s\" protocol=TCP localport=%s" % (name, port)
    try:
        os.popen(delete_port_cmd)
    except:pass
    open_rule_cmd = "netsh advfirewall firewall add rule name=\"%s\" protocol=TCP dir=in localport=%s action=allow" % (name, port)
    os.popen(open_rule_cmd)


if __name__ == "__main__":
    add_rule("mira", 10011)

