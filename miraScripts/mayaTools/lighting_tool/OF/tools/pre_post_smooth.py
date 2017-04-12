import maya.cmds as mc

def preSmooth():
    meshes = mc.ls(type='mesh')
    if meshes:
        for mesh in meshes:
            smoothState = mc.displaySmoothness(mesh, q=1, polygonObject=1)
            if smoothState:
                if smoothState[0] == 3:
                    mc.displaySmoothness(mesh, polygonObject=1)
                    #smoothNode = mc.polySmooth(mesh, ch=1, dv=3)
                    #mc.rename(smoothNode,'smoothNode_'+mesh)
                    mc.setAttr('%s.aiSubdivType' % mesh, 1)
                    mc.setAttr('%s.aiSubdivIterations' % mesh, 2)
                

def postSmooth():
    smoothNodes = mc.ls(type='polySmoothFace')
    if smoothNodes:
        for smoothNode in smoothNodes:
            if smoothNode[:12] == 'smoothNode':
                mesh = mc.listConnections(smoothNode+'.output')
                mc.polySmooth(mesh, e=1, dv=0)
                mc.delete(smoothNode)
                mc.displaySmoothness(mesh, polygonObject=3)
        mc.select(clear=True)

