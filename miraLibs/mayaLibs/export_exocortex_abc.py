# -*- coding: utf-8 -*-
import os
import maya.cmds as mc


def export_exocortex_abc(filename, start, end, objects, uvs=0, facesets=0, purepointcache=1, ogawa=1):
    """
    :param filename: abc path
    :param start: start frame
    :param end: end frame
    :param objects: transform list, must transform node, not shape node
    :param uvs: whether export uv
    :param facesets: whether export facesets
    :return:
    """
    if isinstance(object, basestring):
        objects = [objects]
    file_dir = os.path.dirname(filename)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    file_name_str = "filename=%s" % filename
    in_str = "in=%s" % start
    out_str = "out=%s" % end
    uvs_str = "uvs=%s" % uvs
    facesets_str = "facesets=%s" % facesets
    purepointcache_str = "purepointcache=%s" % purepointcache
    ogawa_str = "ogawa=%s" % ogawa
    objects_str = "objects=%s" % ",".join(objects)
    j_list = [file_name_str, in_str, out_str, uvs_str, facesets_str, purepointcache_str, ogawa_str, objects_str]
    j_str = ";".join(j_list)
    print j_str
    mc.ExocortexAlembic_export(j=[j_str])


if __name__ == "__main__":
    meshes = mc.listRelatives("char_xiaotuotuo_MODEL", ad=1, type="mesh")
    geo = [mc.listRelatives(mesh, p=1)[0] for mesh in meshes]
    geo = list(set(geo))
    export_exocortex_abc("D:/test.abc", 1, 50, geo)
