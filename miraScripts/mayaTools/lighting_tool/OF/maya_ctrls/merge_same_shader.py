#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import maya.cmds as mc
try:
    from PySide import QtGui, QtCore
except:
    from PySide import QtGui, QtCore
import maya.mel as mel
from public_ctrls import undo
    

def get_sg_objects(sg):
    sg_set = sg + '.dagSetMembers'
    sg_me_ele = mc.listConnections(sg_set, s=1, d=0, p=1)

    real_obj = []
    if not sg_me_ele:
        return real_obj

    for sme in sg_me_ele:
        obj_grp_id = sme+'.objectGroupId'
        comp_obj_grp_id = sme+'.compObjectGroupId'
        query_id = []
        if mc.objExists(obj_grp_id):
            query_id.append(obj_grp_id)
        elif mc.objExists(comp_obj_grp_id):
            query_id.append(comp_obj_grp_id)

        if not query_id:
            temp_obj = sme.split('.')[0]
            real_obj = real_obj + [temp_obj]
        else:
            for queryId in query_id:
                tem = mc.listConnections(queryId, s=1, d=0)
                if not tem:
                    temp_obj = sme.split('.')[0]
                    real_obj = real_obj + [temp_obj]
                    continue

                grp_id = tem[0]
                temp_obj_set = mc.createNode('objectSet')

                mc.connectAttr(sme, (temp_obj_set + '.dagSetMembers'), na=1)
                mc.connectAttr((grp_id + '.message'), (temp_obj_set + '.groupNodes'))

                temp_obj = mc.sets(temp_obj_set, q=1)
                if temp_obj:
                    real_obj = real_obj + temp_obj

                in_cons = mc.listConnections(temp_obj_set, s=1, d=0, c=1, p=1)
                for i in range(0, len(in_cons), 2):
                    mc.disconnectAttr(in_cons[i + 1], in_cons[i])

                mc.delete(temp_obj_set)

    real_obj = list(set(real_obj))
    return real_obj


@undo.undo
def merge_same_shader():
    sg_nodes = mc.ls(type='shadingEngine')
    while True:
        if sg_nodes:
            basic_sg_node = sg_nodes.pop(0)
            for sg_node in sg_nodes:
                print "compare %s    to    %s" % (basic_sg_node, sg_node)
                cmp = mc.shadingNetworkCompare(basic_sg_node, sg_node)
                result = mc.shadingNetworkCompare(cmp, q=1, eq=1)
                if result:
                    print "get objects of %s" % sg_node
                    objects = get_sg_objects(sg_node)
                    if objects:
                        mc.sets(objects, e=1, fe=basic_sg_node)
                    sg_nodes.remove(sg_node)
                    print '[OF] info: merge %s<=====>%s' % (basic_sg_node, sg_node)
        else:
            break


def get_maya_win():
    import maya.OpenMayaUI as mui
    if 'PyQt4' in QtGui.__name__:
        import sip
        prt = mui.MQtUtil.mainWindow()
        return sip.wrapinstance(long(prt), QtGui.QWidget)
    elif 'PySide' in QtGui.__name__:
        import shiboken
        prt = mui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(prt), QtGui.QWidget)

            
class MergeSameShader(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MergeSameShader, self).__init__(parent)
        self.setObjectName('Merge Same Shaders')
        self.setWindowTitle('Merge Same Shaders')
        self.resize(300, 70)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        main_layout = QtGui.QVBoxLayout(self)
        self.merge_btn = QtGui.QPushButton('Merge Same Shaders')
        self.delete_btn = QtGui.QPushButton('Delete Unused Nodes')
        main_layout.addWidget(self.merge_btn)
        main_layout.addWidget(self.delete_btn)
        self.set_signals()

    def set_signals(self):
        self.merge_btn.clicked.connect(self.merge)
        self.delete_btn.clicked.connect(self.do_delete)
        
    def merge(self):
        print "==================================start merging================================="
        merge_same_shader()
        print "=================================merge finished================================="

    def do_delete(self):
        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

    @classmethod
    def show_ui(cls):
        if mc.window('Merge Same Shaders', q=1, ex=1):
            mc.deleteUI('Merge Same Shaders')
        mss = cls(get_maya_win())
        mss.show()


def main():
    MergeSameShader.show_ui()

    
if __name__ == '__main__':
    main()