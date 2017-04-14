# -*- coding: utf-8 -*-
import os
import get_engine


class PathGetter(object):
    def __init__(self):
        self.package_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
        self.engine = get_engine.get_engine()
        self.check_conf_engine_dir = None
        self.check_options_engine_dir = None
        self.configuration_dir = None
        self.icon_dir = None

    def get_check_dir(self, dir_type):
        check_dir = os.path.join(self.package_dir, dir_type)
        return check_dir.replace("\\", "/")

    def get_engine_dir(self, dir_type):
        engine_dir = os.path.join(self.get_check_dir(dir_type), self.engine)
        engine_dir = engine_dir.replace("\\", "/")
        return engine_dir

    @classmethod
    def parse_path(cls):
        pg = cls()
        pg.check_conf_engine_dir = pg.get_engine_dir("check_conf")
        pg.check_options_engine_dir = pg.get_engine_dir("check_options")
        pg.configuration_dir = pg.get_check_dir("configuration")
        pg.icon_dir = pg.get_check_dir("icons")
        return pg
