import maya.cmds as mc


def set_default_outliner():
    out_liners = mc.getPanel(type="outlinerPanel")
    for out_liner in out_liners:
        mc.outlinerEditor(out_liner, e=1, setFilter="defaultSetFilter")
