# -*- coding: utf-8 -*-
import maya.cmds as mc


def set_image_format_ar(image_format):
    mc.setAttr('defaultArnoldDriver.aiTranslator', image_format, type='string')


if __name__ == "__main__":
    pass
