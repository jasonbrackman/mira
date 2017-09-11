import maya.cmds as mc


def get_maya_version():
    maya_version = mc.about(version=1)
    return maya_version
