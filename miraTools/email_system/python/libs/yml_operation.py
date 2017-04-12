# -*- coding: utf-8 -*-
import os
import yaml


def get_yaml_data(path):
    with open(path, "r") as f:
        data = yaml.load(f)
        return data


def set_yaml_path(yaml_path, data):
    yaml_dir = os.path.dirname(yaml_path)
    if not os.path.isdir(yaml_dir):
        os.makedirs(yaml_dir)
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)


if __name__ == "__main__":
    pass
