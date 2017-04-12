# -*- coding: utf-8 -*-
import os
import logging
from PySide import QtGui, QtCore
import task_get_ui
reload(task_get_ui)
from miraLibs.sgLibs import Sg
from miraLibs.pipeLibs.pipeMaya import get_current_project
from miraLibs.pipeLibs import pipeMira, pipeHistory, pipeFile
from miraLibs.pyLibs import copy
from miraLibs.osLibs import get_run_app


class Node(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = list()
        self._parent = parent
        if parent:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
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


class EntityNode(Node):
    def __init__(self, name, parent=None):
        super(EntityNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "entity"


class AssetTypeNode(Node):
    def __init__(self, name, parent=None):
        super(AssetTypeNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "asset_type"


class SequenceNode(Node):
    def __init__(self, name, parent=None):
        super(SequenceNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "sequence"


class AssetNode(Node):
    def __init__(self, name, step, task, status, parent):
        super(AssetNode, self).__init__(name, parent)
        self.name = name
        self.step = step
        self.task = task
        self.status = status

    @property
    def node_type(self):
        return "asset"


class ShotNode(Node):
    def __init__(self, name, step, task, status, parent):
        super(ShotNode, self).__init__(name, parent)
        self.name = name
        self.step = step
        self.task = task
        self.status = status

    @property
    def node_type(self):
        return "shot"


class AssetTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, root_node=None, project=None, parent=None):
        super(AssetTreeModel, self).__init__(parent)
        self.root_node = root_node
        self.project = project

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.root_node

    def rowCount(self, parent):
        parent_node = self.getNode(parent)
        return parent_node.childCount()

    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0 and node.node_type == "entity":
                return node.name
            if index.column() == 0 and node.node_type in ["asset_type", "sequence"]:
                return node.name
            if index.column() == 2 and node.node_type in ["asset", "shot"]:
                value = "name:  %s\n"\
                        "step:  %s\n" \
                        "task:  %s\n" \
                        "status:  %s\n" % (node.name, node.step, node.task, node.status)
                return value
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 1 and node.node_type in ["asset", "shot"]:
                if node.node_type == "asset":
                    pix_map_path = pipeFile.get_asset_task_image_file(self.project, node.parent().name,
                                                                      node.name, node.step, node.task)
                else:
                    pix_map_path = pipeFile.get_shot_task_image_file(self.project, node.parent().name,
                                                                     node.name, node.step, node.task)
                if os.path.isfile(pix_map_path):
                    pix_map = QtGui.QPixmap(pix_map_path)
                else:
                    pix_map = QtGui.QPixmap(100, 100)
                    pix_map.fill(QtCore.Qt.black)
                scaled = pix_map.scaled(QtCore.QSize(100, 90), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                return scaled
        elif role == QtCore.Qt.SizeHintRole:
            if node.node_type in ["entity", "asset_type", "sequence"]:
                return QtCore.QSize(30, 20)
            else:
                return QtCore.QSize(100, 100)

    def setData(self, index, value, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == QtCore.Qt.EditRole:
            if index.column() == 0:
                node.name = value
                return True
        return False

    # def headerData(self, section, orientation, role):
    #     header_list = ["entity", "Asset Type/Sequence", "Thumbnail", "Information"]
    #     if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
    #         return header_list[section]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def parent(self, index):
        node = self.getNode(index)
        parent_node = node.parent()
        if parent_node == self.root_node:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        parent_node = self.getNode(parent)
        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()


class LeafFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        super(LeafFilterProxyModel, self).__init__()
        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setFilterKeyColumn(-1)
        self.final_checked = False

    def filterAcceptsRow(self, row_num, source_parent):
        if self.filter_accepts_row_itself(row_num, source_parent):
            return True
        if self.filter_accepts_any_parent(source_parent):
            return True
        return self.has_accepted_children(row_num, source_parent)

    def filter_accepts_row_itself(self, row_num, parent):
        final_index = self.sourceModel().index(row_num, 2, parent)
        index_data = final_index.data()
        is_final = "status:  fin" not in index_data if index_data else False
        filter_result = super(LeafFilterProxyModel, self).filterAcceptsRow(row_num, parent)
        if self.final_checked:
            return filter_result
        else:
            return is_final and filter_result

    def filter_accepts_any_parent(self, parent):
        while parent.isValid():
            if self.filter_accepts_row_itself(parent.row(), parent.parent()):
                return True
            parent = parent.parent()
        return False

    def has_accepted_children(self, row_num, parent):
        model = self.sourceModel()
        source_index = model.index(row_num, 0, parent)
        children_count = model.rowCount(source_index)
        for i in xrange(children_count):
            if self.filterAcceptsRow(i, source_index):
                return True
        return False


class TaskGet(task_get_ui.TaskGetUI):
    def __init__(self, parent=None):
        super(TaskGet, self).__init__(parent)
        self.setObjectName("TaskGet")
        self.__logger = logging.getLogger("TaskGet")
        self.__project = get_current_project.get_current_project()
        self.__sg = Sg.Sg(self.__project)
        self.init()
        self.set_style()
        self.set_model()
        self.set_signals()

    def init(self):
        self.task_view.setSortingEnabled(True)
        self.task_view.setFocusPolicy(QtCore.Qt.NoFocus)
        self.task_view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.task_view.header().hide()
        # init project
        projects = pipeMira.get_projects()
        self.project_cbox.addItems(projects)
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(self.__project))

    def set_style(self):
        run_app = get_run_app.get_run_app()
        if run_app != "python":
            self.local_file_widget.setStyleSheet("QTreeView:item{height: 30px;}")
            self.work_file_widget.setStyleSheet("QTreeView:item{height: 30px;}")
            self.publish_file_widget.setStyleSheet("QTreeView:item{height: 30px;}")
            return
        qss_path = os.path.abspath(os.path.join(__file__, "..", "style.qss"))
        self.setStyle(QtGui.QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

    def set_signals(self):
        self.project_cbox.currentIndexChanged[str].connect(self.on_project_changed)
        self.task_view.clicked.connect(self.show_path)
        self.work_file_widget.copy_to_local_action.triggered.connect(self.copy_to_local)

    def on_project_changed(self, text):
        self.__project = text
        self.refresh()

    def refresh(self):
        self.set_model()
        self.local_file_widget.clear()
        self.work_file_widget.clear()
        self.publish_file_widget.clear()

    def copy_to_local(self):
        file_paths = self.work_file_widget.get_selected()
        if not file_paths:
            return
        file_path = file_paths[0]
        if not os.path.isfile(file_path):
            return
        try:
            obj = pipeFile.PathDetails.parse_path(file_path)
            project = obj.project
            local_path = obj.local_work_file
            copy.copy(file_path, local_path)
            self.local_file_widget.set_dir(os.path.dirname(os.path.dirname(local_path)))
            self.update_task_status(project, file_path)
        except RuntimeError as e:
            logging.error(str(e))

    def update_task_status(self, project, file_path):
        from miraLibs.sgLibs import Tk
        tk = Tk.Tk(project)
        task = tk.get_task_from_path(file_path)
        if not task:
            logging.warning("Can't get task from %s" % file_path)
            return
        self.__sg.update_task_status(task, "ip")

    def set_model(self):
        self.root_node = Node("Task get")
        my_tasks = self.__sg.get_my_tasks()
        if not my_tasks:
            self.model = QtGui.QStandardItemModel()
            self.task_view.setModel(self.model)
            return
        entity_types = [task["entity"]["type"] for task in my_tasks]
        entity_types = list(set(entity_types))
        if "Asset" in entity_types:
            asset_entity_node = EntityNode("Asset", self.root_node)
        if "Shot" in entity_types:
            shot_eneity_node = EntityNode("Shot", self.root_node)
        asset_type_nodes = list()
        sequence_nodes = list()
        for task in my_tasks:
            if task["entity"]["type"] == "Asset":
                asset_type_name = task["entity"]["sg_asset_type"]
                if asset_type_name not in asset_type_nodes:
                    asset_type_node = AssetTypeNode(asset_type_name, asset_entity_node)
                asset_type_nodes.append(asset_type_name)
                asset_name = task["entity"]["code"]
                step = task["step"]["short_name"]
                task_name = task["content"]
                status = task["sg_status_list"]
                asset_node = AssetNode(asset_name, step, task_name, status, asset_type_node)
            else:
                sequence_name = task["entity"]["sg_sequence"]["name"]
                if sequence_name not in sequence_nodes:
                    sequence_node = SequenceNode(sequence_name, shot_eneity_node)
                sequence_nodes.append(sequence_node)
                shot = task["entity"]["code"]
                step = task["step"]["short_name"]
                task_name = task["content"]
                status = task["sg_status_list"]
                shot_node = ShotNode(shot, step, task_name, status, sequence_node)

        self.proxy_model = LeafFilterProxyModel()
        self.model = AssetTreeModel(self.root_node, self.__project)
        self.proxy_model.setSourceModel(self.model)
        self.task_view.setModel(self.proxy_model)
        self.task_view.expandAll()
        self.filter_le.textChanged.connect(self.filter_name)
        self.final_checkbox.stateChanged.connect(self.filter_status)

    def filter_status(self, state):
        self.proxy_model.final_checked = state
        self.proxy_model.reset()
        self.task_view.expandAll()

    def filter_name(self, text):
        self.proxy_model.setFilterRegExp(text)
        self.task_view.expandAll()

    def show_path(self, index):
        node = self.proxy_model.mapToSource(index).internalPointer()
        if node.node_type == "asset":
            asset_type = node.parent().name
            asset_name = node.name
            step = node.step
            task = node.task
            local_file = pipeFile.get_asset_task_work_file(self.__project, asset_type, asset_name, step, task, "000", local=True)
            work_file = pipeFile.get_asset_task_work_file(self.__project, asset_type, asset_name, step, task, "000")
            publish_file = pipeFile.get_asset_task_publish_file(self.__project, asset_type, asset_name, step, task, "000")
        elif node.node_type == "shot":
            sequence = node.parent().name
            shot = node.name.split("_")[-1]
            step = node.step
            task = node.task
            local_file = pipeFile.get_shot_task_work_file(self.__project, sequence, shot, step, task, "000", local=True)
            work_file = pipeFile.get_shot_task_work_file(self.__project, sequence, shot, step, task, "000")
            publish_file = pipeFile.get_shot_task_publish_file(self.__project, sequence, shot, step, task, "000")
        else:
            return
        local_dir = os.path.dirname(os.path.dirname(local_file))
        work_dir = os.path.dirname(os.path.dirname(work_file))
        publish_dir = os.path.dirname(os.path.dirname(publish_file))
        self.local_file_widget.set_dir(local_dir)
        self.work_file_widget.set_dir(work_dir)
        self.publish_file_widget.set_dir(publish_dir)

    def closeEvent(self, event):
        pipeHistory.set("currentProject", self.__project)


def run_standalone():
    import sys
    app = QtGui.QApplication(sys.argv)
    tg = TaskGet()
    tg.show()
    app.exec_()


def run_maya():
    import maya.cmds as mc
    from miraLibs.mayaLibs import get_maya_win
    if mc.window("TaskGet", q=1, ex=1):
        mc.deleteUI("TaskGet")
    tg = TaskGet(get_maya_win.get_maya_win("PySide"))
    tg.show()


if __name__ == "__main__":
    run_standalone()
