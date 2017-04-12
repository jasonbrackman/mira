# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mel


def get_udims():
    sel_objects = mc.ls(sl=1)
    udims = list()
    for sel_object in sel_objects:
        mc.select(sel_object, r=1)
        mel.eval("PolySelectConvert 4;")
        uv_value = mc.polyEditUVShell(q=1)
        if not uv_value:
            udims.append(1000)
            continue
        uv_value_sort = [uv_value[::2], uv_value[1::2]]
        u_max = max(uv_value_sort[0])
        v_max = max(uv_value_sort[1])
        udim = 1000+(v_max-1)*10 + u_max
        udim = round(udim, 1)
        udims.append(udim)
    return udims


if __name__ == "__main__":
    pass
