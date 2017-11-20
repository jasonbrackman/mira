# -*- coding: utf-8 -*-
import maya.cmds as mc


def import_exocortex_abc(file_name, normals=1, attachToExisting=1, uvs=0, facesets=1, multi=0):
    file_name_str = "filename=%s" % file_name
    normals_str = "normal=%s" % normals
    attach_str = "attachToExisting=%s" % attachToExisting
    uvs_str = "uvs=%s" % uvs
    facesets_str = "facesets=%s" % facesets
    multi_str = "multi=%s" % multi
    j_list = [file_name_str, normals_str, attach_str, uvs_str, facesets_str, multi_str]
    j_str = ";".join(j_list)
    print j_str
    mc.ExocortexAlembic_import(j=[j_str])
