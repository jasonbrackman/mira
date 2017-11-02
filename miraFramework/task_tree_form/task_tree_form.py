# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from task_tree_model import TaskTreeModel, ProxyModel
from miraFramework.combo import ProjectCombo
from miraFramework.Filter import Filter
from miraLibs.dbLibs import db_api


STEPS = ["VfxLay", "Vfx", "LgtLay", "Lgt"]


class Node(object):
    def __init__(self, name, node_type, parent=None):
        self._name = name
        self._node_type = node_type
        self._children = list()
        self._parent = parent
        if parent:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent:
            return self._parent._children.index(self)

    def isValid(self):
        return False

    def node_type(self):
        return self._node_type


class TaskTreeForm(QWidget):
    tree_item_clicked = Signal(list)

    def __init__(self, parent=None):
        super(TaskTreeForm, self).__init__(parent)
        self.setup_ui()
        self.proxy_model = ProxyModel()
        self.set_model()
        self.set_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        project_layout = QHBoxLayout()
        project_label = QLabel("Project")
        project_label.setFixedWidth(50)
        self.project_combo = ProjectCombo()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_combo)

        self.filter_le = Filter()

        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)

        main_layout.addLayout(project_layout)
        main_layout.addWidget(self.filter_le)
        main_layout.addWidget(self.tree_view)

    def set_signals(self):
        self.filter_le.textChanged.connect(self.set_filter)
        self.tree_view.pressed.connect(self.emit_selected)

    def set_filter(self, value):
        self.proxy_model.setFilterRegExp(value)
        if value:
            self.tree_view.expandAll()
        else:
            self.tree_view.collapseAll()

    @property
    def project(self):
        return self.project_combo.currentText()

    def set_model(self):
        if not self.project:
            return
        db = db_api.DbApi(self.project).db_obj
        sequences = db.get_all_sequences()
        sequences.sort()
        if not sequences:
            model = QStandardItemModel()
            self.tree_view.setModel(model)
        else:
            root_node = Node("TaskTree", "root")
            for sequence in sequences:
                sequence_node = Node(sequence, "sequence", root_node)
                shots = db.get_all_shots(sequence)
                if not shots:
                    continue
                shots = [shot.get("code") for shot in shots]
                shots.sort()
                for shot in shots:
                    shot_node = Node(shot, "shot", sequence_node)
                    for step in STEPS:
                        step_node = Node(step, "step", shot_node)
            model = TaskTreeModel(root_node)
            self.proxy_model.setSourceModel(model)
            self.tree_view.setModel(self.proxy_model)
            self.tree_view.setSortingEnabled(True)

    def emit_selected(self, index):
        index = self.proxy_model.mapToSource(index)
        node = index.internalPointer()
        emit_list = []
        if node.node_type() == "step":
            emit_list = [self.project, node.parent().parent().name(), node.parent().name(), node.name()]
        self.tree_item_clicked.emit(emit_list)


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(TaskTreeForm)


if __name__ == "__main__":
    main()
