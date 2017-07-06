# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.OpenMayaUI as OpenMayaUI
from miraLibs.pyLibs import yml_operation
from miraLibs.pyLibs import join_path
import miraCore


def get_hud_conf():
    hud_conf_dir = miraCore.get_conf_dir()
    hud_conf_path = join_path.join_path2(hud_conf_dir, "hud.yml")
    hud_data = yml_operation.get_yaml_data(hud_conf_path)
    return hud_data


def cam_call_back(*args):
    if mc.headsUpDisplay("hud_camera", ex=1):
        mc.headsUpDisplay("hud_camera", refresh=1)
    if mc.headsUpDisplay("hud_focal_length", ex=1):
        mc.headsUpDisplay("hud_focal_length", refresh=1)


class HeadsUpDisplay(object):
    def __init__(self, camera=None):
        self.__camera = camera
        if not self.__camera:
            self.__camera = mc.lookThru(q=1)
        else:
            mc.lookThru(self.__camera)
        self.__hud_dict = get_hud_conf()
        self.__huds = self.__hud_dict.keys()
        self.__hud_color = self.__hud_dict["color"]
        self.__huds.remove("color")

        OpenMayaUI.MUiMessage.addCameraChangedCallback("modelPanel4", cam_call_back)

    @property
    def camera(self):
        return self.__camera

    @camera.setter
    def camera(self, value):
        self.__camera = value

    @staticmethod
    def remove_my_hud(hud_name):
        if mc.headsUpDisplay(hud_name, ex=1):
            mc.headsUpDisplay(hud_name, rem=1)

    @staticmethod
    def hide_default_hud():
        all_huds = mc.headsUpDisplay(q=1, lh=1)
        if all_huds:
            for hud in all_huds:
                mc.headsUpDisplay(hud, e=1, vis=0)

    def clear(self):
        # ----hide all huds---- #
        self.hide_default_hud()
        # ----remove my huds---- #
        for hud in self.__huds:
            self.remove_my_hud(hud)
        # ----clear refresh expression---- #
        if mc.objExists("hudRefresh*"):
            mc.delete("hudRefresh")

    def show(self, *args):
        if not self.__camera:
            self.__camera = mc.lookThru(q=1)
        # ----clear old huds---- #
        self.clear()
        # ----look through current camera ----#
        mc.lookThru(self.__camera)
        # ----set hud color ---- #
        mc.displayColor("headsUpDisplayLabels", self.__hud_color["label_color"])
        mc.displayColor("headsUpDisplayValues", self.__hud_color["value_color"])
        # ----create huds---- #
        for hud in self.__huds:
            label = self.__hud_dict[hud]["label"]
            section = self.__hud_dict[hud]["section"]
            block = mc.headsUpDisplay(nextFreeBlock=section)
            labelWidth = self.__hud_dict[hud]["labelWidth"]
            # event = self.__hud_dict[hud]["event"]
            labelFontSize = self.__hud_dict[hud]["labelFontSize"]
            dataFontSize = self.__hud_dict[hud]["dataFontSize"]
            blockSize = self.__hud_dict[hud]["blockSize"]
            command = self.__hud_dict[hud]["command"].format(camera=self.__camera)
            mc.headsUpDisplay(hud, label=label, section=section, block=block, labelWidth=labelWidth,
                              labelFontSize=labelFontSize, dataFontSize=dataFontSize,
                              blockSize=blockSize, attachToRefresh=True, command=command)


if __name__ == "__main__":
    pass
