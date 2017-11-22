# -*- coding: utf-8 -*-
import maya.cmds as mc
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from miraLibs.mayaLibs import Assembly


class SwitchAssembly(QDialog):
    def __init__(self, parent=None):
        super(SwitchAssembly, self).__init__(parent)
        self.assembly = Assembly.Assembly()
        self.reps = self.assembly.get_all_reps()
        self.resize(300, 80)
        self.setWindowTitle("Switch Assembly")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        sel_layout = QHBoxLayout()
        self.sel_btn_group = QButtonGroup()
        all_check = QCheckBox("All")
        all_check.setChecked(True)
        sel_check = QCheckBox("Selected")
        for check in [all_check, sel_check]:
            self.sel_btn_group.addButton(check)
            sel_layout.addWidget(check)
        self.assembly_btn = QPushButton("Assembly")
        self.menu = QMenu()
        self.action_group = QActionGroup(self)
        main_layout.addLayout(sel_layout)
        main_layout.addWidget(self.assembly_btn)

        self.set_signals()

    @property
    def selected_mod(self):
        return self.sel_btn_group.checkedButton().text()

    def set_signals(self):
        self.assembly_btn.pressed.connect(self.create_menu)
        self.action_group.triggered.connect(self.do_switch)

    def create_menu(self):
        if not self.reps:
            return
        self.menu.clear()
        for rep in self.reps:
            rep_action = self.action_group.addAction(rep)
            self.menu.addAction(rep_action)
        self.menu.exec_(QCursor.pos())

    def do_switch(self, action):
        rep = action.text()
        selected = None if self.selected_mod == "All" else True
        self.set_active(rep, selected)

    @staticmethod
    def get_all_ar_nodes(selected=None):
        if selected:
            selected_objs = mc.ls(sl=1)
            if not selected_objs:
                raise RuntimeError("Selected something")
            sel_ar_nods = mc.listRelatives(selected_objs, ad=1, type="assemblyReference")
            all_nodes = selected_objs + sel_ar_nods
            ar_nodes = mc.ls(all_nodes, type="assemblyReference")
            ar_nodes = list(set(ar_nodes))
        else:
            ar_nodes = mc.ls(type="assemblyReference")
        return ar_nodes

    def set_active(self, rep, selected=None):
        ar_nodes = self.get_all_ar_nodes(selected)
        progress_dialog = QProgressDialog('Switch Assembly, Please wait......', 'Cancel', 0, len(ar_nodes))
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumWidth(600)
        progress_dialog.show()
        for index, ar_node in enumerate(ar_nodes):
            progress_dialog.setValue(index)
            reps = mc.assembly(ar_node, q=1, listRepresentations=1)
            if rep not in reps:
                print "%s not in the representations of node %s" % (rep, ar_node)
                continue
            active_label = mc.assembly(ar_node, q=1, activeLabel=1)
            if active_label == rep:
                print "Current active label is %s" % rep
                continue
            mc.assembly(ar_node, e=1, activeLabel=rep)
            if progress_dialog.wasCanceled():
                break


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(SwitchAssembly)


if __name__ == "__main__":
    main()





