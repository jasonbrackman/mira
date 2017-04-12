# coding=utf-8
# __author__ = "heshuai"
# description="""  """


import os
import cPickle as p


def get_cpickle_data(path):
    data = list()
    if os.path.isfile(path):
        with open(path, 'r') as f:
            data = p.load(f)
        return data


def set_cpickle_data(path, data):
    with open(path, 'w') as f:
        p.dump(data, f)

