import logging
import maya.cmds as mc


def reassign_shader():
    selected = mc.ls(sl=1)
    if not selected:
        logging.error("Select something first.")
        return
    root_name = selected[0]
    shapes = mc.listRelatives(root_name, ad=1, type="mesh")
    transforms = [mc.listRelatives(shape, parent=1)[0] for shape in shapes]
    transforms = list(set(transforms))
    for transform in transforms:
        children = mc.listRelatives(transform, s=1)
        if len(children) == 1:
            continue
        ni_shape, shape = children[:2]
        sg_node = mc.listConnections(ni_shape, s=0, d=1, type="shadingEngine")
        if not sg_node:
            continue
        mc.sets(shape, fe=sg_node[0])


if __name__ == "__main__":
    reassign_shader()
