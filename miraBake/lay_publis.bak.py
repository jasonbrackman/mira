# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.pyLibs import json_operation


def get_json_path():
    return "D:/test.json"


def get_main_curve():
    curves = mc.ls(type='nurbsCurve')
    curves = [mc.listRelatives(curve, parent=1)[0] for curve in curves]
    return curves


def get_anim_data():
    curves = get_main_curve()
    curve_list = list()
    if not curves:
        return
    for curve in curves:
        anim_curves = mc.listConnections(curve, type="animCurve", s=1, d=0)
        if not anim_curves:
            continue
        for anim_curve in anim_curves:
            attributes = mc.listConnections(anim_curve, s=0, d=1, p=1)
            if not attributes:
                continue
            full_attribute = attributes[0]
            frames = mc.keyframe(anim_curve, timeChange=1, q=1)
            if not frames:
                continue
            for frame in frames:
                value = mc.getAttr(full_attribute, time=frame)
                curve_list.append([full_attribute, frame, value])
    return curve_list


def export_anim_data():
    json_path = get_json_path()
    anim_data = get_anim_data()
    json_operation.set_json_data(json_path, anim_data)
    tip_message = "Export json data: %s" % json_path
    print tip_message
    logging.info(tip_message)


if __name__ == "__main__":
    export_anim_data()
