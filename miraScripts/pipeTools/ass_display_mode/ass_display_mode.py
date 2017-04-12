#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'
from PySide import QtGui, QtCore
import maya.cmds as cmd
from miraLibs.mayaLibs import get_maya_win


class StandInViewUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(StandInViewUI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName('StandinViewState')
        self.setWindowTitle(self.tr('StandinViewState'))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        """@create layout"""
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)

        view_mode_layout = QtGui.QHBoxLayout()

        standin_tree_layout = QtGui.QVBoxLayout()

        button_layout = QtGui.QHBoxLayout()

        """@create widget"""
        view_mode_label = QtGui.QLabel(self.tr('View Mode'))
        view_mode_label.setMaximumWidth(view_mode_label.sizeHint().width())

        self.__view_mode_comboBox = QtGui.QComboBox()
        model = QtGui.QStandardItemModel()

        view_mode = {0: 'Bounding Box', 1: 'Per Object Bounding Box', 2: 'PolyWire', 3: 'Wireframe', 4: 'Point Cloud',
                     5: 'Shader PolyWire', 6: 'Shaded'}

        for key, value in view_mode.iteritems():
            item = QtGui.QStandardItem(value)
            model.appendRow(item)
        self.__view_mode_comboBox.setModel(model)

        self.__standin_tree = QtGui.QTreeWidget()
        self.__standin_tree.setColumnCount(1)
        self.__standin_tree.setHeaderLabels(['Tree'])
        self.__standin_tree.clear()
        self.__standin_tree.setHeaderHidden(True)
        self.__standin_tree.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.__standin_tree.itemSelectionChanged.connect(self.clicked_standin_list_item)

        self.init_list()

        set_view_pushbutton = QtGui.QPushButton('-->> Do <<--')
        rest_pushbutton = QtGui.QPushButton('-->> Reset <<--')

        self.connect(set_view_pushbutton, QtCore.SIGNAL('clicked()'), self.set_view_state)
        self.connect(rest_pushbutton, QtCore.SIGNAL('clicked()'), self.reset_ui)

        view_mode_layout.addWidget(view_mode_label)
        view_mode_layout.addWidget(self.__view_mode_comboBox)
        standin_tree_layout.addWidget(self.__standin_tree)
        button_layout.addWidget(set_view_pushbutton)
        button_layout.addWidget(rest_pushbutton)
        main_layout.addLayout(view_mode_layout)
        main_layout.addLayout(standin_tree_layout)
        main_layout.addLayout(button_layout)

    def init_list(self):
        for standin in cmd.ls('standin*', transforms=True):
            root_node = QtGui.QTreeWidgetItem(self.__standin_tree)
            root_node.setText(0, standin)
            standin_object_list = cmd.listRelatives(standin, type='transform')
            if standin_object_list is not None:
                for standin_object in standin_object_list:
                    sub_node = QtGui.QTreeWidgetItem(root_node)
                    sub_node.setText(0, standin_object)

            self.__standin_tree.addTopLevelItem(root_node)

    def clicked_standin_list_item(self):
        sel = []
        for selectedItem in self.__standin_tree.selectedItems():
            sel.append(selectedItem.text(0))
        if sel is not []:
            cmd.select(sel, replace=True)

    def set_view_state(self):
        for selectedItem in self.__standin_tree.selectedItems():
            all_standin = cmd.listRelatives(selectedItem.text(0), allDescendents=True, type="aiStandIn")
            if all_standin is not None:
                for standin in all_standin:
                    cmd.setAttr('%s.mode' % standin, self.__view_mode_comboBox.currentIndex())

    def reset_ui(self):
        self.__view_mode_comboBox.setCurrentIndex(0)
        self.__standin_tree.clear()
        self.__standin_tree.clearSelection()
        self.init_list()


def main():
    if cmd.pluginInfo('mtoa.mll', q=True, loaded=True):
        if not cmd.window("StandinViewState", ex=1):
            standin_view_window = StandInViewUI(get_maya_win.get_maya_win("PySide"))
            standin_view_window.show()
    else:
        QtGui.QMessageBox.critical(None, "Critical", 'have no mtoa.mll')


if __name__ == "__main__":
    main()
