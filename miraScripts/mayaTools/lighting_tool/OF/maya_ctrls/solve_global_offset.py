# coding=utf-8
# __author__ = "guoyang"
# description="""  """

import maya.cmds as cmds

#alembic_node_types = ("bs_alembicNode", )

special_node_types = ("shaveHair", )


def fix_inherits_transform(nodes, state):
    for node in nodes:
        cmds.setAttr("%s.inheritsTransform" % node, state)

def get_camera_center(objs):
    cams = cmds.ls(objs, dag = 1, et = "camera")
    if not cams: return 0, 0, 0
    cams = cmds.listRelatives(cams, p = 1, pa = 1)

    x, y, z = 0, 0, 0
    for cam in cams:
        cam_x, cam_y, cam_z = cmds.xform(cam, q = 1, t = 1, ws = 1)
        x += cam_x; y += cam_y; z += cam_z
    x = x / len(cams); y = y / len(cams); z = z / len(cams)
    return x, y, z

def global_transform(objs, center):
    grp = cmds.group(n = "global_offset_grp", em = 1)
    cmds.parent(objs, grp)
    cmds.xform(grp, t = (-center[0], 0, -center[2]), ws = 1)
    return grp

def get_top_level_objects():
    result = list()
    for obj in cmds.ls(assemblies = 1):
        if obj not in ("persp", "top", "front", "side"):
            result.append(obj)
    return result

def insert_transform_offset(node):
    conns = cmds.listConnections("%s.translate" % node, s = 1, d = 0, p = 1, c = 1)

    if conns:
        offset = cmds.shadingNode("plusMinusAverage", n = "global_offset_Node#", au = 1)
        cmds.connectAttr(conns[1], "%s.input3D[0]" % offset, f = 1)
        cmds.connectAttr("%s.output3D" % offset, "%s.translate" % node, f = 1)

    else:
        connx = cmds.listConnections("%s.tx" % node, s = 1, d = 0, p = 1, c = 1)
        conny = cmds.listConnections("%s.ty" % node, s = 1, d = 0, p = 1, c = 1)
        connz = cmds.listConnections("%s.tz" % node, s = 1, d = 0, p = 1, c = 1)

        offset = cmds.shadingNode("plusMinusAverage", n = "global_offset_Node#", au = 1)

        for index, conns in enumerate((connx, conny, connz)):
            if not conns:
                value = cmds.getAttr("%s.t%s" % (node, "xyz"[index]))
                cmds.setAttr("%s.input3D[0].input3D%s" % (offset, "xyz"[index]), value)
            else:
                cmds.connectAttr(conns[1], "%s.input3D[0].input3D%s" % (offset, "xyz"[index]), f = 1)
        cmds.connectAttr("%s.output3D" % offset, "%s.translate" % node, f = 1)

    return offset

def get_not_inherits_transform():
    nodes = list()
    for trans in cmds.ls(tr = 1):
        if not cmds.getAttr("%s.inheritsTransform" % trans):
            nodes.append(trans)
    return nodes

def set_current_renderlayer(layer):
    cmds.editRenderLayerGlobals(crl = layer)

def solve_global_offset():
    if cmds.objExists("global_offset_grp"): return

    set_current_renderlayer("defaultRenderLayer")

    nodes = get_not_inherits_transform()
    offset_nodes = list()
    if nodes:
        for node in nodes:
            offset = insert_transform_offset(node)
            offset_nodes.append(offset)

    nodes = list()
    try:
        nodes = cmds.ls(et = special_node_types)
    except:pass
    if nodes:
        trans = cmds.listRelatives(nodes, p = 1, pa = 1)
        fix_inherits_transform(trans, state = False)

    objs = get_top_level_objects()
    center = get_camera_center(objs)
    group = global_transform(objs, center)

    if offset_nodes:
        for offset in offset_nodes:
            cmds.connectAttr("%s.translate" % group, "%s.input3D[1]" % offset, f = 1)
        print ">>> Solve Global Offset Done"




if __name__ == '__main__':
    solve_global_offset()

