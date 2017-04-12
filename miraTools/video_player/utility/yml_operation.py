# -*- coding: utf-8 -*-
import yaml


def get_yaml_data(path):
    with open(path, "r") as f:
        data = yaml.load(f)
        return data


def set_yaml_path(yaml_path, data):
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)


if __name__ == "__main__":
    pass
