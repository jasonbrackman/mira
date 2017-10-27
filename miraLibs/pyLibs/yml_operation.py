# -*- coding: utf-8 -*-
import re
import os
import yaml


def get_yaml_data(path):
    if not os.path.isfile(path):
        return
    with open(path, "r") as f:
        data = yaml.load(f)
        return data


def set_yaml_path(yaml_path, data):
    yaml_dir = os.path.dirname(yaml_path)
    if not os.path.isdir(yaml_dir):
        os.makedirs(yaml_dir)
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)


class DeepConfParser(object):
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def _load(yaml_str):
        return yaml.load(yaml_str)

    def load_file(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                data = self._load(f)
                return data
        return None

    def parse_includes(self, origin_dict):
        includes_dict = dict()
        if origin_dict. has_key("includes"):
            includes = origin_dict["includes"]
            for include in includes:
                include_file_path = os.path.abspath(os.path.join(os.path.dirname(self.file_path), include))
                include_file_path.replace("\\", "/")
                each_dict = self.load_file(include_file_path)
                includes_dict.update(each_dict)
        return includes_dict

    def parse(self):
        origin_dict = self.load_file(self.file_path)
        include_dict = self.parse_includes(origin_dict)
        with open(self.file_path, "r") as f:
            strings = f.read()
        if include_dict:
            for key in include_dict:
                if "@%s" % key in strings:
                    strings = re.sub("@%s" % key, include_dict[key], strings)
        after_include_dict = self._load(strings)
        for key in after_include_dict:
            if "@%s" % key in strings:
                strings = re.sub("@%s" % key, after_include_dict[key], strings)
        new_dict = self._load(strings)
        return new_dict


if __name__ == "__main__":
    pass
