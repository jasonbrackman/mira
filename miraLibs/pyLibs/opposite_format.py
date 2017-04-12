# -*- coding: utf-8 -*-
import re


def opposite_format(template, path):
    flags = re.findall("{\w+}", template)
    flags = [flag.lstrip("{").rstrip("}") for flag in flags]
    template_pattern = template.replace(".", "\.")
    pattern = re.sub("{\w+}", "(.*)", template_pattern)
    values = re.match(pattern, path).groups()
    return dict(zip(flags, values))
