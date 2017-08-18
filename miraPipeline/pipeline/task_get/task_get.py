# -*- coding: utf-8 -*-
import os
import logging
import imp
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import task_get_ui
reload(task_get_ui)
import miraCore
from miraLibs.dbLibs import db_api
from miraLibs.pipeLibs import pipeHistory, pipeFile
from miraLibs.pyLibs import copy, join_path
from miraLibs.osLibs import get_engine
from miraLibs.pipeLibs.pipeDb import task_from_db_path
from miraLibs.qtLibs.create_round_rect_thumbnail import create_round_rect_thumbnail


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


class TaskNode(Node):
    def __init__(self, project, entity_type, entity_name, step, task, status, status_color, due_date, priority, parent):
        super(TaskNode, self).__init__(entity_name, parent)
        self.project = project
        self.entity_type = entity_type
        self.entity_name = entity_name
        self.step = step
        self.task = task
        self.status = status
        self.status_color = status_color
        self.due_date = due_date
        self.priority = priority
        self.image = self.get_image()

    @property
    def node_type(self):
        return "task"

    def get_image(self):
        image_path = pipeFile.get_task_workImage_file(self.project, self.entity_type, self.parent().name,
                                                      self.name, self.step, self.task)
        if not image_path or not os.path.isfile(image_path):
            image_path = os.path.abspath(os.path.join(__file__, "..", "unknown.png")).replace("\\", "/")
        scaled = create_round_rect_thumbnail(image_path, 100, 70, 10)
        return scaled


class AssetTreeModel(QAbstractItemModel):
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
        if role == Qt.DisplayRole:
            if index.column() == 0 and node.node_type == "entity":
                return node.name
            if index.column() == 0 and node.node_type in ["asset_type", "sequence"]:
                return node.name
            if index.column() == 2 and node.node_type in ["task"]:
                value = "name:  %s\n"\
                        "step:  %s\n" \
                        "task:  %s\n" \
                        "status:  %s\n"\
                        "priority: %s" % (node.name, node.step, node.task, node.status, node.priority)
                return value
        elif role == Qt.DecorationRole:
            if index.column() == 1 and node.node_type in ["task"]:
                return node.image
        elif role == Qt.SizeHintRole:
            if node.node_type in ["entity", "asset_type", "sequence"]:
                return QSize(10, 20)
            else:
                return QSize(100, 90)

    def setData(self, index, value, role):
        if not index.isValid():
            return
        node = index.internalPointer()
        if role == Qt.EditRole:
            if index.column() == 0:
                node.name = value
                return True
        return False

    # def headerData(self, section, orientation, role):
    #     header_list = ["entity", "Asset Type/Sequence", "Thumbnail", "Information"]
    #     if role == Qt.DisplayRole and orientation == Qt.Horizontal:
    #         return header_list[section]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def parent(self, index):
        node = self.getNode(index)
        parent_node = node.parent()
        if parent_node == self.root_node:
            return QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        parent_node = self.getNode(parent)
        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()


class LeafFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super(LeafFilterProxyModel, self).__init__()
        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setSortCaseSensitivity(Qt.CaseInsensitive)
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
        is_final = "status:  Delivered" not in index_data if index_data else False
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
        self.__engine = get_engine.get_engine()
        self.__db = db_api.DbApi(self.project).db_obj
        self.init()
        self.set_style()
        self.set_model()
        self.set_signals()
        self.selected = None

    @property
    def project(self):
        return self.project_cbox.currentText()

    def init(self):
        self.task_view.setSortingEnabled(True)
        self.task_view.setFocusPolicy(Qt.NoFocus)
        self.task_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.task_view.header().hide()

    def set_style(self):
        if self.__engine != "python":
            self.local_file_widget.setStyleSheet("QTreeView:item{height: 30px;}")
            self.work_file_widget.setStyleSheet("QTreeView:item{height: 30px;}")
            self.publish_file_widget.setStyleSheet("QTreeView:item{height: 30px;}")
            return
        qss_path = os.path.abspath(os.path.join(__file__, "..", "style.qss"))
        self.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())

    def set_signals(self):
        self.project_cbox.currentIndexChanged[str].connect(self.on_project_changed)
        self.task_view.clicked.connect(self.on_item_clicked)
        self.work_file_widget.copy_to_local_action.triggered.connect(self.copy_to_local)
        self.refresh_btn.clicked.connect(self.refresh)
        self.init_btn.clicked.connect(self.init_task)

    def on_project_changed(self, text):
        self.project = text
        self.refresh()

    def refresh(self):
        self.set_model()
        self.local_file_widget.clear()
        self.work_file_widget.clear()
        self.publish_file_widget.clear()
        self.status_label.setText("")
        self.due_label.setText("")

    def copy_to_local(self):
        file_paths = self.work_file_widget.get_selected()
        if not file_paths:
            return
        file_path = file_paths[0]
        if not os.path.isfile(file_path):
            return
        try:
            print file_path
            obj = pipeFile.PathDetails.parse_path(file_path)
            local_path = obj.local_work_path
            copy.copy(file_path, local_path)
            work_dir = os.path.dirname(os.path.dirname(local_path))
            work_engine_dir = join_path.join_path2(work_dir, self.__engine)
            self.local_file_widget.set_dir(work_engine_dir)
            self.update_task_status(file_path)
            self.file_widget.setCurrentIndex(0)
        except RuntimeError as e:
            logging.error(str(e))

    def update_task_status(self, file_path):
        task = task_from_db_path.task_from_db_path(self.__db, file_path)
        self.__db.update_task_status(task, "In progress")
        self.__logger.info("Change task status to In progress.")
        from datetime import datetime
        now_time = datetime.now().strftime('%Y-%m-%d')
        self.__db.update_task(task, sub_date=now_time)
        self.__logger.info("Change task sub date: %s" % now_time)

    def set_model(self):
        self.root_node = Node("Task get")
        my_tasks = self.__db.get_my_tasks()
        print "@"*100
        print my_tasks
        if not my_tasks:
            self.model = QStandardItemModel()
            self.task_view.setModel(self.model)
            return
        if self.__db.typ == "shotgun":
            entity_types = [task["entity"]["type"] for task in my_tasks]
            entity_types = list(set(entity_types))
            if "Asset" in entity_types:
                asset_entity_node = EntityNode("Asset", self.root_node)
            if "Shot" in entity_types:
                shot_entity_node = EntityNode("Shot", self.root_node)
            asset_type_nodes = list()
            sequence_nodes = list()
            for task in my_tasks:
                if task["entity"]["type"] == "Asset":
                    asset_type_names = [node.name for node in asset_type_nodes]
                    asset_type_name = task["entity.Asset.sg_asset_type"]
                    if asset_type_name not in asset_type_names:
                        asset_type_node = AssetTypeNode(asset_type_name, asset_entity_node)
                        asset_type_nodes.append(asset_type_node)
                    else:
                        asset_type_node = [node for node in asset_type_nodes if node.name == asset_type_name][0]
                    asset_name = task["entity.Asset.code"]
                    step = task["step.Step.short_name"]
                    task_name = task["content"]
                    status = task["sg_status_list"]
                    priority = task["sg_priority_1"]
                    asset_node = TaskNode(self.project, "Asset", asset_name, step, task_name, status, priority, asset_type_node)
                else:
                    sequence_names = [node.name for node in sequence_nodes]
                    sequence_name = task["entity.Shot.sg_sequence"]["name"]
                    if sequence_name not in sequence_names:
                        sequence_node = SequenceNode(sequence_name, shot_entity_node)
                        sequence_nodes.append(sequence_node)
                    else:
                        sequence_node = [node for node in sequence_nodes if node.name == sequence_name][0]
                    shot = task["entity.Shot.code"]
                    step = task["step.Step.short_name"]
                    task_name = task["content"]
                    status = task["sg_status_list"]
                    priority = task["sg_priority_1"]
                    shot_node = TaskNode(self.project, shot, step, task_name, status, priority, sequence_node)
        elif self.__db.typ == "strack":
            entity_types = [self.__db.get_task_entity_type(task) for task in my_tasks]
            entity_types = list(set(entity_types))
            print entity_types
            if "Asset" in entity_types:
                asset_entity_node = EntityNode("Asset", self.root_node)
            if "Shot" in entity_types:
                shot_entity_node = EntityNode("Shot", self.root_node)
            asset_type_nodes = list()
            sequence_nodes = list()
            for task in my_tasks:
                task_entity_type = self.__db.get_task_entity_type(task)
                print task_entity_type
                task_entity_id = task.get("item_id")
                task_entity_name = task.get("item").get("item_name")
                task_name = task.get("name")
                step = task.get("step").get("name")
                status = task.get("status").get("name")
                status_color = task.get("status").get("color")
                due_date = task.get("due_date")
                priority = task.get("priority")
                if task_entity_type == "Asset":
                    print task_entity_id, "ka"
                    asset_type_names = [node.name for node in asset_type_nodes]
                    asset_type_name = self.__db.get_asset_type_by_asset_id(task_entity_id)
                    print asset_type_name
                    if asset_type_name not in asset_type_names:
                        asset_type_node = AssetTypeNode(asset_type_name, asset_entity_node)
                        asset_type_nodes.append(asset_type_node)
                    else:
                        asset_type_node = [node for node in asset_type_nodes if node.name == asset_type_name][0]
                    asset_node = TaskNode(self.project, task_entity_type, task_entity_name, step, task_name, status,
                                          status_color, due_date, priority, asset_type_node)
                else:
                    sequence_names = [node.name for node in sequence_nodes]
                    sequence_name = self.__db.get_sequence_by_shot_id(task_entity_id)
                    print sequence_name
                    if sequence_name not in sequence_names:
                        sequence_node = SequenceNode(sequence_name, shot_entity_node)
                        sequence_nodes.append(sequence_node)
                    else:
                        sequence_node = [node for node in sequence_nodes if node.name == sequence_name][0]
                    shot_node = TaskNode(self.project, task_entity_type, task_entity_name, step, task_name, status,
                                         status_color, due_date, priority, sequence_node)
        self.proxy_model = LeafFilterProxyModel()
        self.model = AssetTreeModel(self.root_node, self.project)
        self.proxy_model.setSourceModel(self.model)
        self.task_view.setModel(self.proxy_model)
        self.task_view.expandAll()
        self.task_view.setColumnWidth(0, 80)
        self.filter_le.textChanged.connect(self.filter_name)
        self.final_checkbox.stateChanged.connect(self.filter_status)

    def filter_status(self, state):
        self.proxy_model.final_checked = state
        # self.proxy_model.reset()
        self.proxy_model.invalidateFilter()
        self.task_view.expandAll()

    def filter_name(self, text):
        self.proxy_model.setFilterRegExp(text)
        self.task_view.expandAll()

    def on_item_clicked(self, index):
        node = self.proxy_model.mapToSource(index).internalPointer()
        self.selected = node
        if node.node_type != "task":
            return
        entity_type = node.entity_type
        asset_type_sequence = node.parent().name
        asset_name_shot = node.name.split("_")[-1]
        step = node.step
        task = node.task
        status = node.status
        status_color = node.status_color
        due_date = node.due_date
        # show path
        local_file = pipeFile.get_task_work_file(self.project, entity_type, asset_type_sequence, asset_name_shot, step,
                                                 task, "000", engine=self.__engine, local=True)
        work_file = pipeFile.get_task_work_file(self.project, entity_type, asset_type_sequence, asset_name_shot, step,
                                                task, "000", engine=self.__engine, )
        publish_file = pipeFile.get_task_publish_file(self.project, entity_type, asset_type_sequence, asset_name_shot,
                                                      step, task, "000", engine=self.__engine, )
        local_dir = os.path.dirname(os.path.dirname(local_file))
        work_dir = os.path.dirname(os.path.dirname(work_file))
        publish_dir = os.path.dirname(os.path.dirname(publish_file))
        if self.__engine != "python":
            local_dir = join_path.join_path2(local_dir, self.__engine)
            work_dir = join_path.join_path2(work_dir, self.__engine)
            publish_dir = join_path.join_path2(publish_dir, self.__engine)
        print local_dir, work_dir, publish_dir
        self.local_file_widget.set_dir(local_dir)
        self.work_file_widget.set_dir(work_dir)
        self.publish_file_widget.set_dir(publish_dir)
        # show status and due_date
        self.status_label.setText("<font size=4 color=%s><b>%s</b></font>" % (status_color, status))
        self.due_label.setText("<font size=4 color=#ff8c00>%s</font>" % due_date)

    def init_task(self):
        node = self.selected
        if not node:
            return
        if node.node_type != "task":
            return
        work_file = pipeFile.get_task_work_file(node.project, node.entity_type, node.parent().name, node.entity_name,
                                                node.step, node.task, version="001", engine=self.__engine)
        context = pipeFile.PathDetails.parse_path(work_file)
        local_file = context.local_work_path
        if os.path.isfile(local_file):
            msg = QMessageBox.information(self, "Warming Tip", "%s already exist\nDo you want to replace it?" % local_file,
                                          QMessageBox.Yes | QMessageBox.No)
            if msg.name == "No":
                return
            else:
                self.do_init_task(node, local_file)
        else:
            self.do_init_task(node, local_file)

    def do_init_task(self, node, local_file):
        pipeline_dir = miraCore.get_pipeline_dir()
        start_dir = os.path.join(pipeline_dir, self.__engine, "start").replace("\\", "/")
        fn_, path, desc = imp.find_module(node.step, [start_dir])
        mod = imp.load_module(node.step, fn_, path, desc)
        mod.main(local_file, True)
        self.update_task_status(local_file)
        self.status_label.setText("<font size=4 color=#96e8ff><b>In Progress</b></font>")

    def closeEvent(self, event):
        pipeHistory.set("currentProject", self.project)


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(TaskGet)

if __name__ == "__main__":
    main()
