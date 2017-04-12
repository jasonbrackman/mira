# -*- coding: utf-8 -*-
import logging
import os
import shutil


dir_list = [{"T:": r'\\192.168.0.252\3D-backup1'}]


class Copy(object):
    def __init__(self):
        self.logger = logging.getLogger("pipe copy")

    @staticmethod
    def convert_dir(dir_name):
        for dir_dict in dir_list:
            for key in dir_dict:
                if key in dir_name:
                    dir_name = dir_name.replace(key, dir_dict[key])
        dir_name = dir_name.replace("\\", "/")
        return dir_name

    @classmethod
    def create_dir(cls, dir_name):
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
            return True

    @classmethod
    def copy(cls, src_file, tar_file):
        obj = cls()
        if not os.path.isfile(src_file):
            obj.logger.warning("%s is not an exist file." % src_file)
            return
        if os.path.isfile(tar_file):
            obj.logger.warning("%s in an exist file, permission defined" % tar_file)
            return
        # tar_file = obj.convert_dir(tar_file)
        tar_dir = os.path.dirname(tar_file)
        obj.create_dir(tar_dir)
        try:
            shutil.copyfile(src_file, tar_file)
            return True
        except OSError as e:
            obj.logger.error(str(e))
            return False


if __name__ == "__main__":
    Copy.copy(r"D:\test.png", r"T:\sct\prop\test.png")
