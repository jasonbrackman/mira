# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from plant_tree_UI import plant_tree_UI
from miraLibs.mayaLibs import get_maya_win
from functools import partial
import maya.cmds as mc
import maya.OpenMayaUI as omUI
import maya.OpenMaya as om
import re


class PlanTree(plant_tree_UI):
    def __init__(self, parent=None):
        super(PlanTree, self).__init__(parent)
        self.set_additional()

    def set_additional(self):
        self.startBtn.setMinimumHeight(50)
        self.endBtn.setMinimumHeight(50)
        self.set_tree_list()
        self.make_connections()

    def set_tree_list(self):
        if not mc.objExists('standin'):
            QMessageBox.information(self,'error','no standin group,please check it')
            return
        tree_list = mc.listRelatives('standin',c=1)
        for i in tree_list:
            item = QListWidgetItem()
            item.setText(i)
            self.treeListWidget.addItem(item)

    def make_connections(self):
        self.addGroundBtn.clicked.connect(self.add_ground_function)
        self.startBtn.clicked.connect(self.start_plant)
        self.endBtn.clicked.connect(self.close)

    def add_ground_function(self):
        if not mc.ls(sl=1):
            QMessageBox.information(self, 'error', 'select a mesh first')
            return
        ground_trans = mc.ls(sl=1,l=1)[0]
        ground_shape = mc.listRelatives(ground_trans, c=1, f=1)[0]
        if not mc.nodeType(ground_shape) == 'mesh':
            QMessageBox.information(self, 'error', 'this is not a mesh obj')
            return
        self.lineEdit_2.setText(ground_trans)

    def start_plant(self):
        if mc.draggerContext('plantTree',exists = True):
            mc.setToolTo('plantTree')
        else:
            mc.draggerContext( 'plantTree', pressCommand=partial(self.sample_context_press), dragCommand=partial(self.sample_context_drag), cursor='hand')
            mc.setToolTo('plantTree')

    def end_plant(self):
        mc.scriptJob( kill=self.job_number, force=True)

    def sample_context_drag(self):
        pressPosition = mc.draggerContext( 'plantTree', query=True, dragPoint=True)
        self.do_plant(pressPosition)

    def sample_context_press(self):
        pressPosition = mc.draggerContext( 'plantTree', query=True, anchorPoint=True)
        self.do_plant(pressPosition)

    def do_plant(self, pressPosition):
        view = omUI.M3dView.active3dView()
        worldPt = om.MPoint()
        worldVector = om.MVector()
        view.viewToWorld(int(pressPosition[0]),int(pressPosition[1]),worldPt,worldVector)
        mSel = om.MSelectionList()
        mSel.add(self.lineEdit_2.text())
        mDagPath = om.MDagPath()
        mSel.getDagPath(0,mDagPath)
        fnMesh = om.MFnMesh( mDagPath )
        farclip = 1.0
        clickPos = om.MFloatPoint(worldPt.x,worldPt.y,worldPt.z)
        mCamPath = om.MDagPath()
        view.getCamera(mCamPath)
        cam_name = mCamPath.fullPathName()
        ratio_scale = mc.getAttr(cam_name+'.farClipPlane')

        clickDir = om.MFloatVector(worldVector.x*ratio_scale,worldVector.y*ratio_scale,worldVector.z*ratio_scale)
        currentHitFP = om.MFloatPoint()
        hit = fnMesh.closestIntersection( clickPos,clickDir,None,None,True,om.MSpace.kWorld,farclip,True,None,currentHitFP,None,None,None,None,None)
        if hit:
            tree_name = self.treeListWidget.currentItem().text()
            current_namespace = tree_name.split(':')[1].split('_')[1]
            dup_tree = mc.duplicate(tree_name)
            mc.move(currentHitFP.x,currentHitFP.y,currentHitFP.z ,tree_name)

            new_namespace = self.get_namespace(current_namespace)

            mc.namespace(add=new_namespace)

            for i in dup_tree:
                mc.rename(i, "%s:%s" % (new_namespace, i))

    def get_namespace(self,current_namespace):
        namespace_list = [i for i in mc.namespaceInfo(listOnlyNamespaces=1) if i.startswith(current_namespace)]
        namespace_list = sorted(namespace_list, key=lambda x: self.sort_key(x))
        max_namespace = namespace_list[-1]
        current_num = max_namespace.split(current_namespace)[1]
        if current_num =='':
            current_num =0
        namespace_num = int(current_num) + 1
        return current_namespace + str(namespace_num)
    
    @staticmethod
    def sort_key(value):
        str_num = "".join(re.findall(r"\d", value))
        return str_num.zfill(5)


def main():
    maya_win = get_maya_win.get_maya_win("PySide")
    window = PlanTree(maya_win)
    window.show()


if __name__ == "__main__":
    main()
