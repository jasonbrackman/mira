# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omUI


def get_objs_in_camera_view(min_frame, max_frame):
    all_view_obj = []
    view = omUI.M3dView.active3dView()
    for frame in xrange(min_frame, max_frame + 1):
        mc.currentTime(frame, edit=True)
        om.MGlobal.selectFromScreen(0, 0, view.portWidth(), view.portHeight(), om.MGlobal.kReplaceList)
        all_view_obj.extend(mc.ls(sl=1))

    all_view_obj = list(set(all_view_obj))
    return all_view_obj


if __name__ == "__main__":
    print get_objs_in_camera_view(1, 1)
