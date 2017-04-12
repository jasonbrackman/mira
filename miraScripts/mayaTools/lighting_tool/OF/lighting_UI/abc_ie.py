#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import maya.cmds as mc
import os
import sys
import pymel.core as pm
from PySide import QtGui, QtCore
import maya_ctrls
from maya_ctrls import clear_namespace
import shutil
import glob
from public_ctrls import cpickle_operation


NAME = 'abc export and import'


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


def print_info(func):
    def _wrapper(*args, **kwargs):
        print '*'*100
        print '='*100
        print '*'*100
        print "start run %s" % func.__name__
        func(*args, **kwargs)
        print '*'*100
        print '='*100
        print '*'*100
    return _wrapper


def show_ui(cls):
    instance = cls()
    if mc.window(str(instance.objectName()), q=1, ex=1):
        mc.deleteUI(str(instance.objectName()))
    ui = cls(get_maya_win())
    ui.show()


def get_os_type():
    os_type = None
    if 'win' in sys.platform:
        os_type = 'windows'
    elif 'linux' in sys.platform:
        os_type = 'linux'
    return os_type


def load_plugin():
    if not mc.pluginInfo('AbcExport.mll', q=1, loaded=1):
        mc.loadPlugin('AbcExport.mll', quiet=1)


def get_frame_range():
    return [mc.playbackOptions(q=1, min=1), mc.playbackOptions(q=1, max=1)]


def get_selected_objects():
    selected_objects = []
    for i in mc.ls(sl=1):
        if mc.nodeType(i) in ['mesh', 'nurbsSurface']:
            selected_objects.append(i)
        else:
            if mc.nodeType(i) == 'transform':
                children = mc.ls(i, ap=1, dag=1, lf=1)
                for child in children:
                    if mc.nodeType(child) in ['mesh', 'nurbsSurface']:
                        selected_objects.append(child)
    selected_objects = list(set(selected_objects))
    return selected_objects


def get_sg_node_of_mesh(mesh):
    return mc.listConnections(mesh, d=1, et=1, t='shadingEngine')


def get_selected_meshes(selected=True):
    if selected:
        meshes = get_selected_objects()
    else:
        meshes = mc.ls(type='mesh')
    return meshes


def add_mat_attr(meshes):
    if meshes:
        for mesh in meshes:
            sg_node = get_sg_node_of_mesh(mesh)[0]
            if 'Matinfo' not in mc.listAttr(mesh):
                mc.addAttr(mesh, ln='Matinfo', dt='string')
            mc.setAttr(mesh+'.Matinfo', sg_node, type='string')
        print "[OF] info: Add attributes successful"
    else:
        print "[OF] info: No meshes"


def export_sg(root_path, selected=True):
    def get_sg_node():
        if selected:
            meshes = get_selected_objects()
            sg_nodes = list()
            for mesh in meshes:
                sg_node = get_sg_node_of_mesh(mesh)
                sg_nodes.extend(sg_node)
        else:
            sg_nodes = mc.ls(type='shadingEngine')
        return list(set(sg_nodes))
    sg_nodes = get_sg_node()
    if sg_nodes:
        try:
            sg_nodes.remove('initialParticleSE')
            sg_nodes.remove('initialShadingGroup')
        except:pass
        for sg_node in sg_nodes:
            mc.select(sg_node, r=1, ne=1)
            sg_file = os.path.join(root_path, sg_node+'.mb')
            mc.file(sg_file, pr=1, es=1, typ='mayaBinary')
        print "[OF] info: export shading group successful"
    else:
        print "[OF] info: No Shading Group"


def export_abc(abc_file_name, start_frame, end_frame, selected=True):
    load_plugin()

    def get_export_objects():
        if selected:
            objects = mc.ls(sl=1)
        else:
            all_trans = mc.ls(assemblies=1)
            cameras = mc.ls(cameras=1)
            cam_trans = [mc.listRelatives(cam, parent=1)[0] for cam in cameras]
            objects = list(set(all_trans)-set(cam_trans))
        return objects
    objects = get_export_objects()
    if not objects:
        return
    abc_file_name = abc_file_name.replace('\\', '/')
    j_string = '-framerange {start_frame} {end_frame} -attr Matinfo ' \
               '-uvWrite -worldSpace -writeVisibility -file {tar_path}'
    j_string = j_string.format(start_frame=start_frame, end_frame=end_frame, tar_path=abc_file_name)
    for i in objects:
        j_string += ' -root %s' % i
    print j_string
    mc.AbcExport(j=j_string)
    print "[OF] info: export abc successful"


def import_materials(root_path):
    material_files = glob.glob('%s/*.mb' % root_path)
    if material_files:
        for f in material_files:
            mc.file(f, i=1)
        print "[OF] info: material import successful"
    else:
        print "[OF] info: No material files found"


def import_abc(abc_file):
    load_plugin()
    if os.path.isfile(abc_file):
        mc.AbcImport(abc_file, mode='import')
        print "[OF] info: abc import successful"
    else:
        print "[OF] info: %s is not an exist file" % abc_file


def assign_material():
    meshes = mc.ls(type='mesh')
    for mesh in meshes:
        try:
            mc.sets(mesh, fe=mc.getAttr(mesh+'.Matinfo'))
        except:pass
    print "[OF] info: assign materials successful"


class Separator(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Separator, self).__init__(parent)
        separator_layout = QtGui.QHBoxLayout(self)
        separator_layout.setContentsMargins(0, 0, 0, 0)
        separator_layout.setAlignment(QtCore.Qt.AlignBottom)
        frame = QtGui.QFrame()
        frame.setFrameStyle(QtGui.QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        separator_layout.addWidget(frame)


class AbcIE(QtGui.QDialog):
    def __init__(self, parent=None):
        super(AbcIE, self).__init__(parent)
        self.setObjectName(NAME)
        self.setWindowTitle(NAME)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.resize(350, 70)

        self.frame_range = get_frame_range()

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setSpacing(15)

        file_layout = QtGui.QHBoxLayout()
        file_label = QtGui.QLabel('abc path')
        file_label.setFixedWidth(45)
        self.abc_file_le = QtGui.QLineEdit()
        self.abc_file_btn = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon))
        self.abc_file_btn.setIcon(icon)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.abc_file_le)
        file_layout.addWidget(self.abc_file_btn)

        export_group = QtGui.QGroupBox('Export Settings')
        export_layout = QtGui.QVBoxLayout(export_group)
        export_layout.setSpacing(12)

        check_layout = QtGui.QHBoxLayout()
        check_layout.setContentsMargins(50, 0, 0, 0)
        self.button_group = QtGui.QButtonGroup()
        self.all_cbox = QtGui.QCheckBox('All')
        self.selected_cbox = QtGui.QCheckBox('Selected')
        self.button_group.addButton(self.all_cbox)
        self.button_group.addButton(self.selected_cbox)
        check_layout.addWidget(self.all_cbox)
        check_layout.addWidget(self.selected_cbox)

        separator = Separator()

        frame_layout = QtGui.QHBoxLayout()
        label = QtGui.QLabel('Frame Range')
        self.start_le = QtGui.QLineEdit()
        self.last_le = QtGui.QLineEdit()
        frame_layout.addWidget(label)
        frame_layout.addWidget(self.start_le)
        frame_layout.addWidget(self.last_le)

        self.export_abc_btn = QtGui.QPushButton('Export Abc Cache')
        self.import_abc_btn = QtGui.QPushButton('Import Abc Cache')

        export_layout.addLayout(check_layout)
        export_layout.addWidget(separator)
        export_layout.addLayout(frame_layout)
        export_layout.addWidget(self.export_abc_btn)

        main_layout.addLayout(file_layout)
        main_layout.addWidget(export_group)
        main_layout.addWidget(self.import_abc_btn)

        self.init_settings()
        self.set_signals()
        self.read_settings()

    def init_settings(self):
        self.selected_cbox.setChecked(True)
        self.start_le.setText(str(self.frame_range[0]))
        self.last_le.setText(str(self.frame_range[1]))

    def set_signals(self):
        self.abc_file_btn.clicked.connect(self.get_abc_path)
        self.abc_file_le.textChanged.connect(self.write_out)
        self.export_abc_btn.clicked.connect(self.export)
        self.import_abc_btn.clicked.connect(self.import_abc)

    def get_abc_path(self):
        file_dialog = QtGui.QFileDialog()
        file_dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        init_dir = '/'
        if self.abc_file_le.text():
            init_dir = os.path.dirname(str(self.abc_file_le.text()))
        file_path, filter = file_dialog.getSaveFileName(self, 'choose abc path', init_dir, 'abc files(*.abc)', option=0)
        if file_path:
            self.abc_file_le.setText(str(file_path))

    def get_latest_dir(self):
        os_type = get_os_type()
        if os_type == 'windows':
            latest_dir = os.path.join(os.environ['APPDATA'], 'latest_abc_file.data')
        elif os_type == 'linux':
            latest_dir = os.path.join('/tmp', 'latest_abc_file.data')
        return latest_dir

    def write_out(self, text):
        latest_dir = self.get_latest_dir()
        cpickle_operation.set_cpickle_data(latest_dir, str(text))

    def read_settings(self):
        latest_dir = self.get_latest_dir()
        if os.path.isfile(latest_dir):
            value = cpickle_operation.get_cpickle_data(latest_dir)
            self.abc_file_le.setText(value)

    @print_info
    def export(self):
        abc_file_path = str(self.abc_file_le.text())
        root_path = os.path.dirname(abc_file_path)
        if self.button_group.checkedButton() == self.all_cbox:
            selected = False
        else:
            selected = True
        first_frame = str(self.start_le.text())
        last_frame = str(self.last_le.text())
        clear_namespace.clear_namespace()
        meshes = get_selected_meshes(selected)
        add_mat_attr(meshes)
        export_abc(abc_file_path, first_frame, last_frame, selected)
        export_sg(root_path, selected)

    @print_info
    def import_abc(self):
        abc_file_path = str(self.abc_file_le.text())
        root_path = os.path.dirname(abc_file_path)
        if os.path.isfile(abc_file_path):
            import_abc(abc_file_path)
            import_materials(root_path)
            assign_material()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.close()


def main():
    show_ui(AbcIE)


if __name__ == '__main__':
    main()