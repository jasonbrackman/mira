# -*- coding: utf-8 -*-
import maya.cmds as mc
from get_file_type import get_file_type


def maya_import(file_path):
    file_type = get_file_type(file_path)
    mc.file(file_path, i=1, type=file_type, ignoreVersion=1, ra=1,
            mergeNamespacesOnClash=0, namespace=":", options="v=0",
            pr=1, importFrameRate=1, importTimeRange="override")
