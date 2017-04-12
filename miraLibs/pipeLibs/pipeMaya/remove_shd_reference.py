# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import assign_lambert, delete_unused_nodes


def remove_shd_reference(delete_nodes=False):
    # remove shd reference
    reference_files = mc.file(q=1, r=1)
    for reference_file in reference_files:
        obj = pipeFile.PathDetails.parse_path(reference_file)
        if obj.is_shd_file():
            mc.file(reference_file, rr=1)
    # assign all meshes lambert
    assign_lambert.assign_lambert()
    if delete_nodes:
        delete_unused_nodes.delete_unused_nodes()
