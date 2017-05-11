# -*- coding: utf-8 -*-
from miraLibs.pipeLibs.pipeMaya import get_current_project
from miraLibs.pipeLibs import pipeMira
import os
import maya.cmds as mc


class CharacterBaseLight:
    def __init__(self):
        self.current_project = get_current_project.get_current_project()
        self.current_root = pipeMira.get_root_dir(self.current_project)
    def import_light(self):
        current_light_path = "%s/%s/lib/light/character_base_light/Cha_light.mb"%(self.current_root,self.current_project)
        if os.path.isfile(current_light_path):
            mc.file(current_light_path,r=1,namespace='cha_light')
        else :
            mc.confirmDialog( title='Error', message='base light not exists' )


def main():
    CharacterBaseLight().import_light()