# -*- coding: utf-8 -*-
import sys
import getpass
from strackConfParser import StrackConfParser


def get_standalone_st():
    conf_data = StrackConfParser.st_conf_data()
    st_api_path = conf_data.get("st_api_path")
    if st_api_path not in sys.path:
        sys.path.insert(0, st_api_path)
    base_url = conf_data.get("base_url")
    login = conf_data.get("login")
    api_key = conf_data.get("api_key")
    from strack_api import strack
    reload(strack)
    user = getpass.getuser()
    if user == "liaolin":
        print "liaolin"
        return strack.Strack(base_url=base_url, login="liaolin", api_key="e9772b96c4f86aa458e981cf58ff3983")
    else:
        return strack.Strack(base_url=base_url, login=login, api_key=api_key)


if __name__ == "__main__":
    print get_standalone_st()
