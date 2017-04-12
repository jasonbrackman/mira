# -*- coding: utf-8 -*-
import maya.cmds as mc


def set_image_size(width, height):
    mc.setAttr('defaultResolution.width', width)
    mc.setAttr('defaultResolution.height', height)
    device_ratio = float(width) / float(height)
    mc.setAttr('defaultResolution.deviceAspectRatio', device_ratio)
    mc.setAttr('defaultResolution.pixelAspect', 1)


if __name__ == "__main__":
    pass
