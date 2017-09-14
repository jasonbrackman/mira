# -*- coding: utf-8 -*-
import os
import json


def get_json_data(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            data = json.loads(f.read())
            return data
    else:
        return False


def set_json_data(path, data):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with open(path, 'w') as f:
        json_data = json.dumps(data)
        f.write(json_data)


if __name__ == "__main__":
    pass
