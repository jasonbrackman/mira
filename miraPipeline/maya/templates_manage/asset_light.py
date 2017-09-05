# -*- coding: utf-8 -*-
from miraLibs.pipeLibs.pipeMaya import get_current_project
from miraLibs.pipeLibs import pipeMira
import os
import maya.cmds as mc


class AssetLight(object):
    def __init__(self):
        self.current_project = get_current_project.get_current_project()
        self.current_root = pipeMira.get_studio_value(self.current_project, "primary")

    def import_char_light(self):
        current_light_path = "%s/%s/templates/assetLights/charLight/char_light.ma" % \
                             (self.current_root, self.current_project)
        if os.path.isfile(current_light_path):
            mc.file(current_light_path, r=1, namespace='char_light')
        else:
            mc.confirmDialog(title='Error', message='base light not exists')

    def import_env_light(self):
        pass
