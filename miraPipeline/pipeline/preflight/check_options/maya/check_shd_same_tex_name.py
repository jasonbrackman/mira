# -*- coding: utf-8 -*-
from miraLibs.pipeLibs.pipeMaya import get_same_base_name_textures
from BaseCheck import BaseCheck


class Check(BaseCheck):

    def run(self):
        self.error_list = get_same_base_name_textures.get_same_base_name_textures()
        print self.error_list
        if self.error_list:
            self.fail_check(u"这些贴图在不同的路径下，有相同的名字")
        else:
            self.pass_check(u"贴图正确")


if __name__ == "__main__":
    pass
