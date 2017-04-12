# -*- coding: utf-8 -*-


def select_current_view_objects():
    import maya.OpenMaya as om
    import maya.OpenMayaUI as mui
    active_view = mui.M3dView.active3dView()
    om.MGlobal.selectFromScreen(0, 0, active_view.portWidth(), active_view.portHeight(), om.MGlobal.kReplaceList)


if __name__ == "__main__":
    pass
