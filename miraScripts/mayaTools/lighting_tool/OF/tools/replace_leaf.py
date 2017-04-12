
from PySide import QtGui, QtCore
import maya.cmds as cmds
import maya.mel as mel
import re
import pymel.core as pm
import maya.OpenMayaUI as mui
import sip


def get_maya_win():
    prt = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(prt), QtGui.QWidget)


def cMuscleSurfAttach(objShape, edgeIdx1, edgeIdx2):
    node = cmds.createNode("cMuscleSurfAttach", n="cMuscleSurfAttachShape#")
    xform = cmds.listRelatives(node, p=1)[0]
    cmds.connectAttr("%s.worldMesh" % objShape, "%s.surfIn" % node, f=1)
    cmds.connectAttr("%s.rotateOrder" % xform, "%s.inRotOrder" % node, f=1)
    cmds.setAttr("%s.uLoc" % node, 0.5)
    cmds.setAttr("%s.vLoc" % node, 0.5)
    cmds.setAttr("%s.edgeIdx1" % node, edgeIdx1)
    cmds.setAttr("%s.edgeIdx2" % node, edgeIdx2)
    cmds.setAttr("%s.inheritsTransform" % xform, 0)
    cmds.connectAttr("%s.outTranslate" % node, "%s.translate" % xform, f=1)
    cmds.connectAttr("%s.outRotate" % node, "%s.rotate" % xform, f=1)
    return xform, node


class ReplaceWidget(QtGui.QDialog):

    def __init__(self, parent=None):
        super(ReplaceWidget, self).__init__(parent)
        self.setWindowTitle('Replace Leaf')
        self.resize(350, 50)
        main_layout = QtGui.QVBoxLayout(self)
        # -----------------------------delete group-----------------------------#
        del_grp = QtGui.QGroupBox('Delete Edges')
        del_layout = QtGui.QVBoxLayout(del_grp)
        self.get_del_edge_layout = GetDeleteEdges()
        self.delete_edge_btn = QtGui.QPushButton('Delete Edges')
        del_layout.addLayout(self.get_del_edge_layout)
        del_layout.addWidget(self.delete_edge_btn)
        # -----------------------------replace group-----------------------------#
        replace_grp = QtGui.QGroupBox('Replace Plane')
        replace_layout = QtGui.QVBoxLayout(replace_grp)
        self.get_del_edge_layout_new = GetDeleteEdges()
        self.get_del_edge_layout_new.btn.setText('Get Two Edges')
        self.replace_plane_btn = QtGui.QPushButton('Replace Plane')
        replace_layout.addLayout(self.get_del_edge_layout_new)
        replace_layout.addWidget(self.replace_plane_btn)
        # -----------------------------Fix group---------------------------#
        fix_grp = QtGui.QGroupBox()
        fix_layout = QtGui.QHBoxLayout(fix_grp)
        self.fix_btn = QtGui.QPushButton('Fix')
        self.delete_btn = QtGui.QPushButton('Delete Locators')
        fix_layout.addWidget(self.fix_btn)
        fix_layout.addWidget(self.delete_btn)
        # -----------------------------------------------------------------------#
        main_layout.addWidget(del_grp)
        main_layout.addWidget(replace_grp)
        main_layout.addWidget(fix_grp)
        self.set_signals()

    def set_signals(self):
        self.delete_edge_btn.clicked.connect(self.deleteEdge)
        self.replace_plane_btn.clicked.connect(self.solveLeaf)
        self.fix_btn.clicked.connect(self.fix)
        self.delete_btn.clicked.connect(self.delete)

    def get_obj_name(self, text):
        name = text.split(',')[0]
        pattern = '(.*)\.e\[.*\]$'
        object_name = re.match(pattern, name).group(1)
        return object_name

    def get_edge_index(self, text):
        pattern = '.*\.e\[(.*)\]$'
        index_list = []
        for i in text.split(','):
            index = re.match(pattern, i).group(1)
            if ':' not in index:
                index_list.append(int(index))
            else:
                index_list.append(int(index.split(':')[0]))
                index_list.append(int(index.split(':')[1]))
        return index_list

    def deleteEdge(self):
        selected_objs = cmds.ls(sl=1)
        all_string = str(self.get_del_edge_layout.line.text())
        old_obj_name = self.get_obj_name(all_string)
        if selected_objs:
            progress_dialog = QtGui.QProgressDialog(
                'Deleting Edges,Please wait......', 'Cancel', 0, len(selected_objs))
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.show()
            value = 0
            for obj in selected_objs:
                progress_dialog.setValue(value)
                if progress_dialog.wasCanceled():
                    break
                try:
                    cmds.select(obj, r=1)
                    obj_edges = re.sub(old_obj_name, obj, all_string)
                    obj_edges = [i for i in obj_edges.split(',')]
                    cmds.select(obj_edges, r=1)
                    cmds.DeleteEdge(ch=0)
                except:
                    pass
                cmds.select(cl=1)
                value += 1

    def solveLeaf(self):
        if not cmds.pluginInfo('MayaMuscle.mll', q=1, loaded=1):
            cmds.loadPlugin('MayaMuscle.mll', quiet=1)
        selected_objs = cmds.ls(sl=1)
        all_string = str(self.get_del_edge_layout_new.line.text())
        old_obj_name = self.get_obj_name(all_string)
        if selected_objs:
            progress_dialog = QtGui.QProgressDialog(
                'Deleting Edges,Please wait......', 'Cancel', 0, len(selected_objs))
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.show()
            value = 0
            self.locator = []
            self.locator_shapes = []
            self.planes = []
            for obj in selected_objs:
                progress_dialog.setValue(value)
                if progress_dialog.wasCanceled():
                    break
                try:
                    obj = pm.PyNode(obj).getShape().name()
                    index = self.get_edge_index(all_string)
                    loc = cMuscleSurfAttach(obj, index[0], index[1])
                    self.locator.append(loc[0])
                    self.locator_shapes.append(loc[1])
                    pnt = loc[0]
                    plane = cmds.polyPlane(
                        w=1, h=1, sx=1, sy=1, ax=(0, 0, 1), ch = 0)[0]
                    self.planes.append(plane)
                    cmds.parent(plane, pnt, r=1)
                except:
                    pass
                value += 1
            cmds.select(clear=1)
            cmds.select(self.planes)

    def fix(self):
        if self.locator_shapes:
            for loc in self.locator_shapes:
                current_value = cmds.getAttr('%s.fixPolyFlip' % loc)
                cmds.setAttr('%s.fixPolyFlip' % loc, not current_value)

    def delete(self):
        if self.planes:
            cmds.parent(self.planes, w=1)
        if self.locator:
            cmds.delete(self.locator)


class GetDeleteEdges(QtGui.QHBoxLayout):

    def __init__(self, parent=None):
        super(GetDeleteEdges, self).__init__(parent)
        self.btn = QtGui.QPushButton('Get Delete Edges')
        self.line = QtGui.QLineEdit()
        self.addWidget(self.btn)
        self.addWidget(self.line)
        self.btn.clicked.connect(self.get_edges)

    def get_edges(self):
        pattern = '.*\.e\[.*\]'
        select_edges = cmds.ls(sl=1)
        if re.match(pattern, ','.join(select_edges)):
            self.line.setText(','.join(select_edges))


def main():
    global rw
    try:
        rw.close()
        rw.deleteLater()
    except:
        pass
    rw = ReplaceWidget(get_maya_win())
    rw.show()


if __name__ == '__main__':
    main()
