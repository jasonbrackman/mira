# -*- coding: utf-8 -*-
import maya.cmds as mc


def get_maya_lights():
    return mc.ls(lights=1)


def get_arnold_lights():
    arnold_lights = list()
    arnold_light_types = ["aiSkyDomeLight", "aiAreaLight", "aiPhotometricLight"]
    for light_type in arnold_light_types:
        lights = mc.ls(type=light_type)
        if not lights:
            continue
        arnold_lights.extend(lights)
    return arnold_lights


def get_all_lights():
    maya_lights = get_maya_lights()
    arnold_lights = get_arnold_lights()
    all_lights = maya_lights + arnold_lights
    return all_lights
