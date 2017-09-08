import maya.cmds as mc


def import_abc(abc_path):
    mc.AbcImport(abc_path)
