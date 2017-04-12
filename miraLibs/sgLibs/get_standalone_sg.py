# -*- coding: utf-8 -*-
import sys
from shotgunConfParser import ShotgunConfParser


def get_standalone_sg():
    conf_data = ShotgunConfParser.sg_conf_data()
    sg_api_path = conf_data.get("sg_api_path")
    if sg_api_path not in sys.path:
        sys.path.insert(0, sg_api_path)
    from shotgun_api3 import Shotgun
    SERVER_PATH = conf_data.get("sg_site")
    SCRIPT_NAME = conf_data.get("script_name")
    SCRIPT_KEY = conf_data.get("api_key")
    return Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)


if __name__ == "__main__":
    pass
