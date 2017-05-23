# -*- coding: utf-8 -*-


def get_format_of_read_node(read_node):
    width = read_node["format"].value().width()
    height = read_node["format"].value().height()
    return "%s*%s" % (width, height)