__author__ = 'heshuai'

from PySide import QtGui, QtCore
import maya_ctrls
import public_ctrls
from get_parent_dir import get_parent_dir
import os
from functools import partial
import pymel.core as pm


class PolygonWidget(QtGui.QDialog):
    def __init__(self, parent=None):
        super(PolygonWidget, self).__init__(parent)
        self.parent_dir = get_parent_dir()
        # y_pos = public_ctrls.get_maya_main_win_pos()[1] + (public_ctrls.get_maya_main_win_size()[1])/4
        # self.move(public_ctrls.get_maya_main_win_pos()[0], y_pos)
        self.setWindowTitle('Set selected meshes Attribute')
        main_layout = QtGui.QVBoxLayout(self)
        frame = QtGui.QFrame()
        main_layout.addWidget(frame)
        frame.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Sunken)
        polygon_layout = QtGui.QGridLayout(frame)
        polygon_layout.setColumnMinimumWidth(2, 0)
        opaque_label = QtGui.QLabel('Arnold Opaque')
        self.opaque_on_button = QtGui.QPushButton('ON')
        self.opaque_off_button = QtGui.QPushButton('OFF')
        primary_label = QtGui.QLabel('Primary Visibility')
        self.primary_on_button = QtGui.QPushButton('ON')
        self.primary_off_button = QtGui.QPushButton('OFF')
        self.cast_shadows_label = QtGui.QLabel('Cast Shadows')
        self.cast_shadows_on_button = QtGui.QPushButton('ON')
        self.cast_shadows_off_button = QtGui.QPushButton('OFF')
        self.receive_shadows_label = QtGui.QLabel('Receive Shadows')
        self.receive_shadows_on_button = QtGui.QPushButton('ON')
        self.receive_shadows_off_button = QtGui.QPushButton('OFF')
        separate1 = QtGui.QGroupBox('Arnold')
        separate1.setStyleSheet("QGroupBox{color:#32CD32;font-size: 20px}")
        separate1.setFlat(True)
        sub_label = QtGui.QLabel('Arnold Subdivision')
        self.sub_type_cbox = QtGui.QComboBox()
        model = QtGui.QStandardItemModel(self.sub_type_cbox)
        for name in ['none', 'catclark', 'linear']:
            item = QtGui.QStandardItem(name)
            model.appendRow(item)
        self.sub_type_cbox.setModel(model)
        self.sub_type_cbox.setCurrentIndex(1)
        self.sub_value_line = QtGui.QLineEdit()
        self.sub_value_line.setStyleSheet('QLineEdit{border: 1px solid #666666;border-radius: 3px;}')
        self.sub_value_line.setFixedWidth(70)
        diffuse_label = QtGui.QLabel('Visible In Diffuse')
        self.diffuse_on_btn = QtGui.QPushButton('ON')
        self.diffuse_off_btn = QtGui.QPushButton('OFF')
        glossy_label = QtGui.QLabel('Visible In Glossy')
        self.glossy_on_btn = QtGui.QPushButton('ON')
        self.glossy_off_btn = QtGui.QPushButton('OFF')
        displace_height_label = QtGui.QLabel('Displacement Height')
        self.displace_height_line = QtGui.QLineEdit()
        self.displace_height_line.setStyleSheet('QLineEdit{border: 1px solid #666666;border-radius: 3px;}')
        separate2 = QtGui.QGroupBox('Hair')
        separate2.setStyleSheet("QGroupBox{color:#32CD32;font-size: 20px}")
        separate2.setFlat(True)
        hair_primary_label = QtGui.QLabel('Primary Visibility')
        self.hair_primary_on_btn = QtGui.QPushButton('ON')
        self.hair_primary_off_btn = QtGui.QPushButton('OFF')
        polygon_layout.addWidget(primary_label, 0, 0)
        polygon_layout.addWidget(self.primary_on_button, 0, 1)
        polygon_layout.addWidget(self.primary_off_button, 0, 2)
        polygon_layout.addWidget(self.cast_shadows_label, 1, 0)
        polygon_layout.addWidget(self.cast_shadows_on_button, 1, 1)
        polygon_layout.addWidget(self.cast_shadows_off_button, 1, 2)
        polygon_layout.addWidget(self.receive_shadows_label, 2, 0)
        polygon_layout.addWidget(self.receive_shadows_on_button, 2, 1)
        polygon_layout.addWidget(self.receive_shadows_off_button, 2, 2)
        polygon_layout.addWidget(separate1, 3, 0, 1, 3)
        polygon_layout.addWidget(sub_label, 4, 0)
        polygon_layout.addWidget(self.sub_type_cbox, 4, 1)
        polygon_layout.addWidget(self.sub_value_line, 4, 2)
        polygon_layout.addWidget(opaque_label, 5, 0)
        polygon_layout.addWidget(self.opaque_on_button, 5, 1)
        polygon_layout.addWidget(self.opaque_off_button, 5, 2)
        polygon_layout.addWidget(diffuse_label, 6, 0)
        polygon_layout.addWidget(self.diffuse_on_btn, 6, 1)
        polygon_layout.addWidget(self.diffuse_off_btn, 6, 2)
        polygon_layout.addWidget(glossy_label, 7, 0)
        polygon_layout.addWidget(self.glossy_on_btn, 7, 1)
        polygon_layout.addWidget(self.glossy_off_btn, 7, 2)
        polygon_layout.addWidget(displace_height_label, 8, 0)
        polygon_layout.addWidget(self.displace_height_line, 8, 1, 1, 2)
        polygon_layout.addWidget(separate2, 9, 0, 1, 3)
        polygon_layout.addWidget(hair_primary_label, 10, 0)
        polygon_layout.addWidget(self.hair_primary_on_btn, 10, 1)
        polygon_layout.addWidget(self.hair_primary_off_btn, 10, 2)
        self.set_background()
        self.setSignals()

    def set_background(self):
        image_path = os.path.join(self.parent_dir, 'icons', 'background_icons', 'polygon.png')
        self.image = QtGui.QImage(image_path)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(self.image.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(self.image.scaled(event.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)

    def setSignals(self):
        self.primary_on_button.clicked.connect(self.set_primary_on)
        self.primary_off_button.clicked.connect(self.set_primary_off)
        self.cast_shadows_on_button.clicked.connect(self.set_cast_shadows_on)
        self.cast_shadows_off_button.clicked.connect(self.set_cast_shadows_off)
        self.receive_shadows_on_button.clicked.connect(self.set_receive_shadows_on)
        self.receive_shadows_off_button.clicked.connect(self.set_receive_shadows_off)
        self.sub_value_line.textChanged.connect(self.set_subdivision)
        self.opaque_on_button.clicked.connect(self.set_opaque_on)
        self.opaque_off_button.clicked.connect(self.set_opaque_off)
        self.diffuse_on_btn.clicked.connect(self.set_diffuse_on)
        self.diffuse_off_btn.clicked.connect(self.set_diffuse_off)
        self.glossy_on_btn.clicked.connect(self.set_glossy_on)
        self.glossy_off_btn.clicked.connect(self.set_glossy_off)
        self.displace_height_line.textChanged.connect(self.set_displacement_height)
        self.hair_primary_on_btn.clicked.connect(partial(self.hair_primary, 1))
        self.hair_primary_off_btn.clicked.connect(partial(self.hair_primary, 0))

    def set_opaque_on(self):
        maya_ctrls.set_opaque(1)

    def set_opaque_off(self):
        maya_ctrls.set_opaque(0)

    def set_primary_on(self):
        maya_ctrls.set_primary(1)

    def set_primary_off(self):
        maya_ctrls.set_primary(0)

    def set_cast_shadows_on(self):
        maya_ctrls.set_cast_shadows(1)

    def set_cast_shadows_off(self):
        maya_ctrls.set_cast_shadows(0)

    def set_receive_shadows_on(self):
        maya_ctrls.set_receive_shadows(1)

    def set_receive_shadows_off(self):
        maya_ctrls.set_receive_shadows(0)

    def set_subdivision(self):
        sub_type = self.sub_type_cbox.currentIndex()
        if self.sub_value_line.text():
            value = int(self.sub_value_line.text())
            maya_ctrls.set_subdivision(sub_type, value)

    def set_diffuse_on(self):
        maya_ctrls.set_diffuse_visible(1)

    def set_diffuse_off(self):
        maya_ctrls.set_diffuse_visible(0)

    def set_glossy_on(self):
        maya_ctrls.set_glossy_visible(1)

    def set_glossy_off(self):
        maya_ctrls.set_glossy_visible(0)

    def set_displacement_height(self, value):
        maya_ctrls.set_displacement_height(int(value))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.close()

    def get_hairs_by_select(self):
        selected_objects = []
        if pm.ls(sl=1):
            for i in pm.ls(sl=1):
                if i.type() in ['hairSystem']:
                    selected_objects.append(i)
                else:
                    if i.type() == 'transform':
                        children = pm.ls(i, ap=1, dag=1, lf=1)
                        for child in children:
                            if child.type() in ['hairSystem']:
                                selected_objects.append(child)
        return selected_objects

    def hair_primary(self, value):
        hairs = self.get_hairs_by_select()
        if hairs:
            for hair in hairs:
                hair.primaryVisibility.set(value)
                

def run():
    global polygon_widget
    try:
        polygon_widget.close()
        polygon_widget.deleteLater()
    except:pass
    polygon_widget = PolygonWidget(public_ctrls.get_maya_win())
    polygon_widget.show()