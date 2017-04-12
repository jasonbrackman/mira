# -*- coding=UTF-8 -*-
# __author__ = "heshuai"
# description="""  """


import json
import os


def get_json_data(path):
    if os.path.isfile(path):
        f = open(path, 'r')
        data = json.loads(f.read())
        f.close()
        return data
    else:
        return False


def set_json_data(path, data):
    f = open(path, 'w')
    json_data = json.dumps(data)
    f.write(json_data)
    f.close()



