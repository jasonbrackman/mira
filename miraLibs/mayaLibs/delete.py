import maya.cmds as mc


def delete(obj):
    if not mc.objExists(obj):
        print "%s does not exist" % obj
        return
    mc.lockNode(obj, l=0)
    mc.delete(obj)
