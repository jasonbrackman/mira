# -*- coding: utf-8 -*-
import os
import sys
import threading
mira_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", ".."))
sys.path.insert(0, mira_dir)
from miraLibs.pyLibs.socketLibs import open_port
from miraLibs.pyLibs import ConfParser


def run_open_port():
    cp = ConfParser.ConfParser(__file__)
    port = cp.conf_data.get("port")
    t = threading.Thread(target=open_port.open_port, args=(port,))
    t.start()
    print "open port done."


if __name__ == "__main__":
    run_open_port()
