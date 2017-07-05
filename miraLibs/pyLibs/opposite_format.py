# -*- coding: utf-8 -*-
import re
import os


def opposite_format(template, path):
    path = path.replace("\\", "/")
    if "/publish/" in path:
        path = os.path.dirname(path)
        template = os.path.dirname(template)
    flags = re.findall("{\w+}", template)
    flags = [flag.lstrip("{").rstrip("}") for flag in flags]
    template_pattern = template.replace(".", "\.")
    pattern = re.sub("{\w+}", "(.*)", template_pattern)
    matched = re.match(pattern, path)
    if matched:
        values = matched.groups()
        return dict(zip(flags, values))
