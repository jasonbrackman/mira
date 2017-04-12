import maya.cmds as mc


all_ref = mc.file(q=1, r=1)
if all_ref:
    for ref in all_ref:
        a = mc.referenceQuery(ref, isLoaded = 1)
        #if a:
        #mc.file(ref, importReference = 1)
        if not a:
            mc.file(ref, removeReference = 1)