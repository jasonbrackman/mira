# coding utf-8
# __author__ = "heshuai"
# description="""  """

import pymel.core as pm
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.OpenMayaUI as mui
import sip
import maya.cmds as mc
from maya_ctrls import get_sg_node_of_selected


def get_maya_win():
    prt = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(prt), QWidget)


def get_material_of_sg(sg):
    try:
        mat = pm.listConnections(pm.PyNode(sg).surfaceShader, source=1, destination=0)[0]
        if mat:
            return [1, mat.name()]
        else:
            message = 'no material connections'
            return [0, message]
    except:
        message = '%s does not exist' % sg
        return [0, message]


def get_meshes_of_sg(sg):
    try:
        pm.PyNode(sg)
    except:
        message = '%s does not exist' % sg
        return [0, message]
    else:
        meshes = []
        inputs = pm.PyNode(sg).inputs()
        for i in inputs:
            if i.type() == 'transform':
                for j in pm.ls(i, ap=1, dag=1, lf=1):
                    if j.type() in ['mesh', 'nurbsSurface']:
                        meshes.append(j.name())
        meshes = list(set(meshes))
        if meshes:
            return [1, meshes]
        else:
            message = 'No mesh connections'
            return [0, message]


def replace_sg(sg):
    if mc.objExists(sg):
        if sg not in ['initialParticleSE', 'initialShadingGroup']:
            new_sg = mc.createNode('shadingEngine')
            mc.nodeCast(sg, new_sg, copyDynamicAttrs=1, swapValues=1, f=1)
            try:
                mc.delete(sg)
            except:
                mc.warning('%s can not be deleted' % sg)
            else:
                mc.rename(new_sg, sg)
                print '[OF] info: %s has been replaced' % sg


class ListWidgetLayout(QVBoxLayout):
    def __init__(self, text=None, parent=None):
        super(ListWidgetLayout, self).__init__(parent)
        self.setSpacing(0)
        self.text = text
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.label.setText('<font color="#00FF00" size=5>%s</font>' % text)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.addWidget(self.label)
        self.addWidget(self.list_widget)
        self.set_signals()

    def set_signals(self):
        self.list_widget.itemSelectionChanged.connect(self.set_select)

    def set_select(self):
        pm.select(clear=1)
        for item in self.list_widget.selectedItems():
            pm.select(str(item.text()), add=1)


class Find(QDialog):
    def __init__(self, parent=None):
        super(Find, self).__init__(parent)
        self.resize(380, 330)
        main_layout = QVBoxLayout(self)
        #----------------------input layout-----------------------#
        input_layout = QHBoxLayout()
        input_label = QLabel()
        input_label.setText('<font color=#00FF00 size=4>sg name:</font>')
        self.input_le = QLineEdit()
        self.input_le.setPlaceholderText("Input a sg name......")
        self.replace_btn = QPushButton('Replace')
        self.replace_btn.setEnabled(False)
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_le)
        input_layout.addWidget(self.replace_btn)
        #----------------------display layout----------------------#
        display_layout = QHBoxLayout()
        display_layout.setSpacing(20)
        self.mat_list_layout = ListWidgetLayout('Material')
        self.mesh_list_layout = ListWidgetLayout('Meshes')
        display_layout.addLayout(self.mat_list_layout)
        display_layout.addLayout(self.mesh_list_layout)
        #----------------------label layout----------------------#
        label_layout = QHBoxLayout()
        label_layout.setSpacing(0)
        self.info_label = QLabel()
        self.info_label.setText('<font color="#00FF00" size=5>[OF] info:</font>')
        self.info_label.setFixedWidth(80)
        self.warning_label = QLabel()
        label_layout.addWidget(self.info_label)
        label_layout.addWidget(self.warning_label)
        #----------------------separate----------------------#
        separate_layout = QHBoxLayout()
        separate_layout.setContentsMargins(30, 5, 30, 5)
        separate = QFrame()
        separate.setStyleSheet("QFrame{color: #000000}")
        separate.setFrameStyle(QFrame.HLine)
        separate_layout.addWidget(separate)
        #----------------------replace button----------------------#
        self.replace_sel_btn = QPushButton('Replace sg node by selected objects')
        self.replace_sel_btn.setStyleSheet("QPushButton{color: #00FF00}")
        font = QFont()
        font.setBold(True)
        self.replace_sel_btn.setFont(font)
        #----------------------------------------------------------#
        main_layout.addLayout(input_layout)
        main_layout.addLayout(display_layout)
        main_layout.addLayout(label_layout)
        main_layout.addLayout(separate_layout)
        main_layout.addWidget(self.replace_sel_btn)
        self.set_signals()

    def set_signals(self):
        self.input_le.editingFinished.connect(self.show_name)
        self.replace_btn.clicked.connect(self.replace)
        self.replace_sel_btn.clicked.connect(self.replace_by_sel_obj)

    def show_name(self):
        self.warning_label.setText('')
        self.mat_list_layout.list_widget.clear()
        self.mesh_list_layout.list_widget.clear()
        sg_name = str(self.input_le.text())
        if sg_name:
            if mc.objExists(sg_name):
                self.replace_btn.setEnabled(True)
            else:
                self.replace_btn.setEnabled(False)
            #-------------------mat----------------------#
            mat = get_material_of_sg(sg_name)
            if mat[0]:
                item = QListWidgetItem(mat[1])
                self.mat_list_layout.list_widget.addItem(item)
            else:
                self.warning_label.setText('<font color="#FF0000" size=5>%s</font>' % mat[1])
            #-------------------mesh----------------------#
            mesh = get_meshes_of_sg(sg_name)
            if mesh[0]:
                for i in mesh[1]:
                    item = QListWidgetItem(i)
                    self.mesh_list_layout.list_widget.addItem(item)
            else:
                self.warning_label.setText('<font color="#FF0000" size=5>%s</font>' % mesh[1])

    def replace(self):
        sg = str(self.input_le.text())
        replace_sg(sg)

    def replace_by_sel_obj(self):
        sg_nodes = get_sg_node_of_selected.get_sg_node_of_selected()
        if sg_nodes:
            for sg_node in sg_nodes:
                replace_sg(sg_node.name())

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()


def main():
    global find
    try:
        find.close()
        find.deleteLater()
    except:pass
    find = Find(get_maya_win())
    find.show()

if __name__ == '__main__':
    main()