# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from miraFramework.task_tree_form import task_tree_form
from miraLibs.pipeLibs import Project


class ListView(QListView):
    left_pressed = Signal(QModelIndex)

    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setFlow(QListView.LeftToRight)
        self.setMovement(QListView.Static)
        self.setFocusPolicy(Qt.NoFocus)
        self.setWrapping(True)
        self.setSpacing(20)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    @property
    def selected(self):
        selected_indexes = self.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = [index.row() for index in selected_indexes]
        selected_rows.sort()
        selected = [self.model().model_data[row] for row in selected_rows]
        return selected


class ToolButton(QToolButton):
    def __init__(self, parent=None):
        super(ToolButton, self).__init__(parent)


class LeftButton(ToolButton):
    def __init__(self, parent=None):
        super(ToolButton, self).__init__(parent)
        self.setMinimumSize(30, 30)
        self.setAutoFillBackground(True)
        icon_path = os.path.abspath(os.path.join(__file__, "..", "icons", "left.png"))
        disable_path = os.path.abspath(os.path.join(__file__, "..", "icons", "left_disable.png"))
        icon = QIcon(icon_path)
        self.setIcon(icon)
        self.setIconSize(QSize(26, 26))
        style_sheet = "QToolButton{background: transparent;border:none;border-radius:15px;}" \
                      "QToolButton:disabled {image: url(%s);}QToolButton:hover{background: #222}" % disable_path
        self.setStyleSheet(style_sheet)


class ListModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.model_data = model_data

    def rowCount(self, parent=QModelIndex()):
        return len(self.model_data)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        item = self.model_data[row]
        if role == Qt.DisplayRole:
            return item.name
        if role == Qt.FontRole:
            return QFont("Arial", 8, QFont.Bold)
        if role == Qt.ForegroundRole:
            return QColor("#fff")
        if role == Qt.ToolTipRole:
            return item.path
        if role == Qt.DecorationRole:
            image = item.image
            return image

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for index, i in enumerate(value):
            self.model_data.insert(position+index, i)
        self.model_data.sort(key=lambda x: x.name)
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.model_data[position]
            self.model_data.remove(value)
        self.endRemoveRows()
        return True

    def setData(self, index, value, role):
        row = index.row()
        if value:
            if role == Qt.DecorationRole:
                self.model_data[row] = value
                self.dataChanged.emit(index, index)
            return True

    def remove_all(self):
        for i in xrange(self.rowCount()):
            self.removeRows(0, 1)


class ListItem(object):
    def __init__(self, name, typ, image, path):
        """
        :param name: name
        :param typ: version or texture
        :param image: thumbnail
        :return: folder full path
        """
        self.name = name
        self.typ = typ
        self.image = image
        self.path = path


class Loader(QDialog):
    def __init__(self, parent=None):
        super(Loader, self).__init__(parent)
        self.work_dir = None
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Loader")
        self.setObjectName("Loader")
        self.resize(700, 600)
        self.setup_ui()
        self.set_signals()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_splitter = QSplitter(Qt.Horizontal)
        self.task_tree_form = task_tree_form.TaskTreeForm()

        texture_widget = QWidget()
        layout = QVBoxLayout(texture_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignLeft)
        self.left_btn = LeftButton()
        self.left_btn.setDisabled(True)
        btn_layout.addWidget(self.left_btn)
        self.tab_widget = QTabWidget()
        self.work_list_view = ListView()
        self.work_list_view.workarea = None
        self.publish_list_view = ListView()
        self.publish_list_view.workarea = "texture"
        self.tab_widget.addTab(self.work_list_view, "work")
        self.tab_widget.addTab(self.publish_list_view, "publish")
        layout.addLayout(btn_layout)
        layout.addWidget(self.tab_widget)

        main_splitter.addWidget(self.task_tree_form)
        main_splitter.addWidget(texture_widget)

        main_splitter.setSizes([self.width()*0.35, self.width()*0.65])
        main_splitter.setStretchFactor(1, 1)
        main_layout.addWidget(main_splitter)

    def set_signals(self):
        self.task_tree_form.tree_item_clicked.connect(self.show_pictures)
        self.work_list_view.doubleClicked.connect(self.on_work_double_clicked)
        self.publish_list_view.doubleClicked.connect(self.on_publish_double_clicked)
        self.left_btn.clicked.connect(self.on_left_btn_clicked)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.work_list_view.customContextMenuRequested.connect(self.show_actions)
        self.publish_list_view.customContextMenuRequested.connect(self.show_actions)

    def set_empty_model(self):
        model = QStandardItemModel()
        self.work_list_view.setModel(model)
        self.publish_list_view.setModel(model)

    def show_pictures(self, value):
        if not value:
            print "has no value"
            self.set_empty_model()
        else:
            project, sequence, shot, step = value
            work_template = Project(project).template("maya_shot_render")
            work_dir = work_template.format(project=project, sequence=sequence, shot=shot.split("_")[-1], step=step)
            publish_template = Project(project).template("maya_shot_renderPublish")
            publish_dir = publish_template.format(project=project, sequence=sequence, shot=shot.split("_")[-1], step=step)
            self.set_dir(work_dir, "work", "version")
            self.set_dir(publish_dir, "publish", "texture")

    @staticmethod
    def __get_icon_dir():
        icon_path = os.path.abspath(os.path.join(__file__, "..", "icons"))
        icon_path = icon_path.replace("\\", "/")
        return icon_path

    def set_dir(self, folder_dir, submit_type, typ):
        if not os.path.isdir(folder_dir):
            if submit_type == "work":
                self.work_list_view.setModel(QStandardItemModel())
            else:
                self.publish_list_view.setModel(QStandardItemModel())
            return
        icon_dir = self.__get_icon_dir()
        icon_path = "%s/folder.png" % icon_dir
        if typ == "texture":
            icon_path = "%s/picture.png" % icon_dir
        pix_map = QPixmap(icon_path).scaled(100, 100, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        dirs = [folder for folder in os.listdir(folder_dir) if os.path.isdir("%s/%s" % (folder_dir, folder))]
        if not dirs:
            if submit_type == "work":
                self.work_list_view.setModel(QStandardItemModel())
            else:
                self.publish_list_view.setModel(QStandardItemModel())
            return
        items = list()
        for d in dirs:
            path = "%s/%s" % (folder_dir, d)
            item = ListItem(d, typ, pix_map, path)
            items.append(item)
        model = ListModel(items)
        if submit_type == "work":
            self.work_list_view.workarea = typ
            self.work_list_view.setModel(model)
        else:
            self.publish_list_view.setModel(model)

    def on_work_double_clicked(self, index):
        if not index.isValid():
            return
        item = index.model().model_data[index.row()]
        folder_dir = item.path
        if item.typ == "version":
            self.set_dir(folder_dir, "work", "texture")
            self.work_dir = folder_dir
            self.left_btn.setDisabled(False)
        else:
            self.load_to_nuke(folder_dir)

    def on_publish_double_clicked(self, index):
        if not index.isValid():
            return
        item = index.model().model_data[index.row()]
        folder_dir = item.path
        self.load_to_nuke(folder_dir)

    @staticmethod
    def load_to_nuke(folder_dir):
        import nuke
        nuke.tcl("drop", folder_dir)

    def on_left_btn_clicked(self):
        self.left_btn.setDisabled(True)
        folder_dir = os.path.dirname(self.work_dir)
        self.set_dir(folder_dir, "work", "version")

    def on_tab_changed(self, index):
        if index == 1:
            self.left_btn.setDisabled(True)
        else:
            if self.work_list_view.workarea == "texture":
                self.left_btn.setDisabled(False)
            else:
                self.left_btn.setDisabled(True)

    def show_actions(self, pos):
        global_pos = self.sender().mapToGlobal(pos)
        self.menu = QMenu(self.sender())
        action_group = QActionGroup(self.sender())
        action_group.triggered.connect(self.on_action_triggered)
        self.show_action = action_group.addAction("Show in FileSystem")
        self.load_action = action_group.addAction("Load in Nuke")
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.load_action)
        self.menu.exec_(global_pos)

    def on_action_triggered(self, action):
        list_view = self.menu.parent()
        selected_items = list_view.selected
        if not selected_items:
            return
        if action is self.show_action:
            item = selected_items[0]
            os.startfile(item.path)
        else:
            if list_view.workarea == "texture":
                for item in selected_items:
                    self.load_to_nuke(item.path)


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(Loader)


if __name__ == "__main__":
    main()
