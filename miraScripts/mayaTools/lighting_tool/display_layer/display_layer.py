# -*- coding: utf-8 -*-
import os
from functools import partial
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
import maya.cmds as mc
from miraLibs.pyLibs import yml_operation


conf_dir = "C:/ProgramData/display_layer"


class CheckBox(QCheckBox):
    def __init__(self, name=None, parent=None):
        super(CheckBox, self).__init__(parent)
        self.data = list()
        self.setText(name)
        self.setChecked(True)
        self.menu = QMenu()
        self.action_group = QActionGroup(self)
        self.add_selected_action = QAction("Add Selected Objects", self)
        self.remove_selected_action = QAction("Remove Selected Objects", self)
        self.select_action = QAction("Select Objects", self)
        self.delete_action = QAction("Delete Layer", self)
        self.action_group.addAction(self.add_selected_action)
        self.action_group.addAction(self.remove_selected_action)
        self.action_group.addAction(self.delete_action)
        self.action_group.addAction(self.select_action)
        self.menu.addAction(self.add_selected_action)
        self.menu.addAction(self.remove_selected_action)
        self.menu.addAction(self.delete_action)
        self.menu.addAction(self.select_action)
        self.action_group.triggered.connect(self.on_triggered)
        self.stateChanged.connect(self.on_state_changed)

    def contextMenuEvent(self, event):
        self.menu.exec_(QCursor.pos())
        event.accept()

    def delete(self):
        if self.data:
            for i in self.data:
                mc.setAttr("%s.visibility" % i, 1)
        self.deleteLater()

    def on_triggered(self, action):
        if action is self.delete_action:
            self.deleteLater()
        elif action is self.add_selected_action:
            selected = mc.ls(sl=1, long=1)
            data = self.data + selected
            self.data = list(set(data))
            if not self.isChecked():
                for i in self.data:
                    mc.setAttr("%s.visibility" % i, 0)
        elif action is self.remove_selected_action:
            selected = mc.ls(sl=1, long=1)
            data = list(set(self.data)-set(selected))
            self.data = data
        elif action is self.select_action:
            mc.select(self.data, r=1)

    def on_state_changed(self, checked):
        if self.data:
            for i in self.data:
                if checked:
                    mc.setAttr("%s.visibility" % i, 1)
                else:
                    mc.setAttr("%s.visibility" % i, 0)


class ToolButton(QToolButton):
    def __init__(self, icon_name=None, parent=None):
        super(ToolButton, self).__init__(parent)
        icon_dir = os.path.join(__file__, "..")
        icon_path = "%s/%s.png" % (icon_dir, icon_name)
        self.setIcon(QIcon(icon_path))
        self.setStyleSheet("QToolButton{background:transparent;border: 0px;}QToolButton:hover{background:#555;}"
                           "QToolButton:pressed{background:#222;}")


class DisplayLayer(QDialog):
    def __init__(self, parent=None):
        super(DisplayLayer, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        self.layers = list()
        self.setWindowTitle("Display layer")
        self.setObjectName("Display layer")
        self.resize(300, 500)

        btn_layout = QHBoxLayout()
        self.add_layer_btn = ToolButton("add")
        self.include_selected_btn = ToolButton("add_selected")
        btn_layout.addStretch()
        btn_layout.addWidget(self.include_selected_btn)
        btn_layout.addWidget(self.add_layer_btn)

        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        widget = QWidget()
        scroll_area.setWidget(widget)
        self.layout = QVBoxLayout(widget)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignTop)

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(scroll_area)

        self.set_signals()

    def set_signals(self):
        self.add_layer_btn.clicked.connect(partial(self.add, False))
        self.include_selected_btn.clicked.connect(partial(self.add, True))

    def do_add(self, name, objects=[]):
        if name not in self.layers:
            check_box = CheckBox(name)
            check_box.data = objects
            self.layout.addWidget(check_box)
            self.layers.append(name)
            return check_box

    def add(self, selected):
        name, ok = QInputDialog.getText(self, "Input", "Input a layer name")
        if not ok:
            return
        if selected:
            objects = mc.ls(sl=1, long=1)
            self.do_add(name, objects)
        else:
            self.do_add(name)

    def closeEvent(self, event):
        if not self.layers:
            return
        if not os.path.isdir(conf_dir):
            os.makedirs(conf_dir)
        scene_name = mc.file(q=1, sn=1)
        if not scene_name:
            return
        conf_file = "%s/%s.yml" % (conf_dir, os.path.splitext(os.path.basename(scene_name))[0])
        conf_dict = dict()
        conf_dict["file_name"] = scene_name
        conf_dict["data"] = list()
        for i in xrange(self.layout.count()):
            layer_widget = self.layout.itemAt(i).widget()
            checked = layer_widget.isChecked()
            objects = layer_widget.data
            layer_data = {"layer": layer_widget.text(), "checked": checked, "objects": objects}
            conf_dict["data"].append(layer_data)
        yml_operation.set_yaml_path(conf_file, conf_dict)

    def showEvent(self, event):
        scene_name = mc.file(q=1, sn=1)
        if not scene_name:
            return
        conf_file = "%s/%s.yml" % (conf_dir, os.path.splitext(os.path.basename(scene_name))[0])
        if not os.path.isfile(conf_file):
            return
        yml_data = yml_operation.get_yaml_data(conf_file)
        if yml_data["file_name"] == scene_name:
            data = yml_data.get("data")
            if not data:
                return
            for i in data:
                layer = i.get("layer")
                checked = i.get("checked")
                objects = i.get("objects")
                check_box = self.do_add(layer, objects)
                check_box.setChecked(checked)


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(DisplayLayer)

