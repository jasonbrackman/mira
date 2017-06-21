# coding utf-8
# __author__ = "heshuai"
# description="""  """


from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import pymel.core as pm
import public_ctrls
import os
from get_parent_dir import get_parent_dir


class AssignHairShader(QDialog):
    def __init__(self, parent=None):
        super(AssignHairShader, self).__init__(parent)
        # y_pos = public_ctrls.get_maya_main_win_pos()[1] + (public_ctrls.get_maya_main_win_size()[1])/4
        # self.move(public_ctrls.get_maya_main_win_pos()[0], y_pos)
        self.setWindowTitle('Assign Hair Shader')
        self.parent_dir = get_parent_dir()
        self.resize(500, 300)
        main_layout = QVBoxLayout(self)
        label_layout = QHBoxLayout()
        label = QLabel()
        label.setText('<font color="#00FF00" size=4><b>These hairs has no shader</b> </font>')
        self.update_btn = QToolButton()
        self.update_btn.setIcon(QIcon(os.path.join(self.parent_dir, 'icons', 'button_icons', 'update.png')))
        self.update_btn.setStyleSheet('QToolButton{background: transparent}')
        label_layout.addWidget(label)
        label_layout.addWidget(self.update_btn)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.list_widget.setSortingEnabled(True)
        self.list_widget.setSpacing(1)
        button_layout = QHBoxLayout()
        self.check_box = QCheckBox('Maya')
        self.diselect_all_btn = QPushButton('Diselect All')
        self.diselect_all_btn.setStyleSheet('QPushButton{color:#CCCCCC; background-color: #222222}')
        self.select_shader_btn = QPushButton('Select Shader')
        self.select_shader_btn.setStyleSheet('QPushButton{color:#CCCCCC; background-color: #222222}')
        self.assign_btn = QPushButton('Assign')
        self.assign_btn.setStyleSheet('QPushButton{color:#CCCCCC; background-color: #222222}')
        button_layout.addWidget(self.check_box)
        button_layout.addStretch()
        button_layout.addWidget(self.diselect_all_btn)
        button_layout.addWidget(self.select_shader_btn)
        button_layout.addWidget(self.assign_btn)
        main_layout.addLayout(label_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(button_layout)
        self.init_settings()
        self.set_background()
        self.set_signals()

    def init_settings(self):
        all_shave_hair = mc.ls(type='shaveHair') + mc.ls(type='hairSystem')
        no_shader_hair = [hair for hair in all_shave_hair if not pm.PyNode(hair).aiHairShader.connections()]
        for hair in no_shader_hair:
            item = QListWidgetItem(hair)
            item.setIcon(QIcon(os.path.join(self.parent_dir, 'icons/main_icons', 'shaveShader.png')))
            self.list_widget.addItem(item)

    def set_signals(self):
        self.list_widget.itemSelectionChanged.connect(self.set_select)
        self.update_btn.clicked.connect(self.update)
        self.diselect_all_btn.clicked.connect(self.diselect_all)
        self.select_shader_btn.clicked.connect(self.select_shader)
        self.assign_btn.clicked.connect(self.assign_shader)

    def set_background(self):
        image_path = os.path.join(self.parent_dir, 'icons', 'background_icons', 'tx.png')
        self.image = QImage(image_path)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.image.scaled(event.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def set_select(self):
        for item in self.list_widget.selectedItems():
            mc.select(str(item.text()), add=1)

    def diselect_all(self):
        for i in xrange(self.list_widget.count()):
            self.list_widget.item(i).setSelected(False)

    def update(self):
        self.list_widget.clear()
        self.init_settings()

    def select_shader(self):
        self.sender().setStyleSheet('QPushButton{color: #00FF00; font-size: 15px; background-color: #300000}')
        select_shader = pm.ls(sl=1)
        if len(select_shader) == 1 and select_shader[0].type() in pm.listNodeTypes('shader'):
            self.select_shader_btn.setText(select_shader[0].name())

    def get_maya_select_list(self):
        selected_objects = []
        if pm.ls(sl=1):
            for i in pm.ls(sl=1):
                if i.type() in ['shaveHair', 'hairSystem']:
                    selected_objects.append(i)
                else:
                    if i.type() == 'transform':
                        children = pm.ls(i, ap=1, dag=1, lf=1)
                        for child in children:
                            if child.type() in ['shaveHair', 'hairSystem']:
                                selected_objects.append(child)
        return selected_objects

    def get_list_widget_items(self):
        return [str(item.text()) for item in self.list_widget.selectedItems()]

    def assign_shader(self):
        if self.check_box.isChecked():
            shave_hairs = list(set(self.get_maya_select_list()))
        else:
            shave_hairs = self.get_list_widget_items()
            shave_hairs = list(set(shave_hairs))
        if shave_hairs:
            if self.select_shader_btn.text() != 'Select Shader':
                shader = pm.PyNode(str(self.select_shader_btn.text()))
                for hair in shave_hairs:
                    pm.PyNode(hair).aiOverrideHair.set(1)
                    shader.outColor >> pm.PyNode(hair).aiHairShader
                    print "[OF] info %s.outColor --------> %s.aiHairShader" % (str(self.select_shader_btn.text()), hair)
                mc.confirmDialog(title='Confirm', message='connect successful', button='OK', cancelButton='OK', icon='information')
            else:
                mc.confirmDialog(title='Confirm', message='Please select a shader', button='OK', cancelButton='OK',icon='information')
                print "[OF] info: Please select a shader"
        else:
            mc.confirmDialog(title='Confirm', message='Please select at least one hair', button='OK', cancelButton='OK',icon='information')
            print "[OF] info: Please select at least one shave hair"
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()


def run():
    global ahs
    try:
        ahs.close()
        ahs.deleteLater()
    except:pass
    ahs = AssignHairShader(public_ctrls.get_maya_win())
    ahs.show()
