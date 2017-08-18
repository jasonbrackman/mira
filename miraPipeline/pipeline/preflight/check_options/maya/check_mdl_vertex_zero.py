# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.mayaLibs import delete_history


class check_mdl_vertex_zero(BaseCheck):

    def run(self):
        selected = mc.ls(sl=1)
        if not selected:
            self.fail_check(u"先手动选中模型大组")
            return
        selected = mc.ls(sl=1)[0]
        meshes = mc.listRelatives(selected, ad=1, type="mesh")
        for mesh in meshes:
            vtx_num = mc.polyEvaluate(mesh, vertex=1)
            if not vtx_num:
                continue
            vertexes = "%s.vtx[0:%s]" % (mesh, vtx_num-1)
            mc.polyMoveVertex(vertexes, ld=(0, 0, 0))
            try:
                delete_history.delete_history()
            except:pass
        mc.select(selected, r=1)
        self.pass_check(u"所有的点已清零")
