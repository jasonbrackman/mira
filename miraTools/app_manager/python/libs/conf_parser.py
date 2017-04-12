# -*- coding: utf-8 -*-
import os
import yaml
import json


class YamlParser(object):
    def __init__(self, path):
        self.path = path

    def get(self):
        if not os.path.isfile(self.path):
            return None
        with open(self.path, "r") as f:
            data = yaml.load(f)
            return data

    def set(self, data):
        yaml_dir = os.path.dirname(self.path)
        if not os.path.isdir(yaml_dir):
            os.makedirs(yaml_dir)
        with open(self.path, "w") as f:
            yaml.dump(data, f)


class JsonParser(object):
    def __init__(self, path):
        self.path = path

    def get(self):
        if os.path.isfile(self.path):
            with open(self.path, 'r') as f:
                data = json.loads(f.read())
                return data
        else:
            return None

    def set(self, data):
        json_dir = os.path.dirname(self.path)
        if not os.path.isdir(json_dir):
            os.makedirs(json_dir)
        with open(self.path, 'w') as f:
            json_data = json.dumps(data)
            f.write(json_data)


class ConfParser(object):
    def __init__(self, path):
        self.path = path.replace("\\", "/")

    def parse(self):
        parser = None
        ext = os.path.splitext(self.path)[-1]
        if ext == ".json":
            parser = JsonParser(self.path)
        elif ext == ".yml":
            parser = YamlParser(self.path)
        else:
            print "add parser -.-"
        return parser


if __name__ == "__main__":
    cp = ConfParser(r"E:\mira\miraTools\app_manager\conf\app_conf_dir.yml")
    print cp.parse().get()
