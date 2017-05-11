# -*- coding: utf-8 -*-
import os
from miraLibs.pyLibs import conf_parser


class CommandOperation(object):
    def __init__(self):
        conf_path = os.path.abspath(os.path.join(__file__, "..", "conf", "command.yml"))
        self.cp = conf_parser.ConfParser(conf_path)

    def get_command(self):
        data = self.cp.parse().get()
        return data

    def set_command(self, **kwargs):
        self.cp.parse().update(**kwargs)
