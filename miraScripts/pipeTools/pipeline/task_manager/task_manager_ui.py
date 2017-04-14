# -*- coding: utf-8 -*-
import re
from PySide import QtGui, QtCore
import miraCore
from miraFramework.Filter import ButtonLineEdit
from miraLibs.pyLibs import join_path


ENGINELIST = ["maya", "nuke", "houdini"]


class ListModel(QtCore.QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__model_data = model_data
        self.__model_data.sort()

    @property
    def model_data(self):
        return self.__model_data

    @model_data.setter
    def model_data(self, value):
        self.__model_data = value

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__model_data)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            return self.__model_data[row]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for i in range(count):
            self.__model_data.insert(position, value)
        self.__model_data.sort()
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.__model_data[position]
            self.__model_data.remove(value)
        self.endRemoveRows()
        return True


class ListView(QtGui.QListView):
    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)
        self.menu = QtGui.QMenu()
        self.remove_action = QtGui.QAction("remove", self)
        self.setSelectionBehavior(QtGui.QListView.SelectRows)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("QListView::item:selected{background: #ff8c00;}")

    def remove_item(self):
        model = self.model()
        if isinstance(model, QtGui.QSortFilterProxyModel):
            model = model.sourceModel()
        selected_indexes = self.selectedIndexes()
        if not selected_indexes:
            return
        count = 0
        selected_indexes = sorted(selected_indexes, key=lambda index: index.row())
        for i in selected_indexes:
            model.removeRows(i.row()-count, 1)
            count += 1

    def clear(self):
        model = self.model()
        if isinstance(model, QtGui.QSortFilterProxyModel):
            model = model.sourceModel()
        model.model_data = list()
        self.setModel(model)

    def get_items_data(self):
        items_data = list()
        model = self.model()
        if isinstance(model, QtGui.QSortFilterProxyModel):
            model = model.sourceModel()
        for i in xrange(model.rowCount(self)):
            model_index = model.index(i, 0)
            data = model_index.data()
            # data = self.list_model.data(model_index, QtCore.Qt.DisplayRole)
            items_data.append(str(data))
        return items_data

    def get_selected(self):
        selected = list()
        proxy_model = self.model()
        selected_indexes = self.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = list(set([proxy_model.mapToSource(i).row() for i in selected_indexes]))
        for row in selected_rows:
            value_index = proxy_model.sourceModel().index(row, 0)
            selected.append(value_index.data())
        return selected


class CommonWidget(QtGui.QWidget):
    add_signal = QtCore.Signal(basestring)

    def __init__(self, parent=None):
        super(CommonWidget, self).__init__(parent)
        self.resize(150, 180)
        self.model_data = list()
        self.group_name = None

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.group_box = QtGui.QGroupBox()
        main_layout.addWidget(self.group_box)
        group_layout = QtGui.QVBoxLayout()

        horizon_layout = QtGui.QHBoxLayout()
        horizon_layout.setSpacing(0)
        icon_dir = miraCore.get_icons_dir()
        icon_path = join_path.join_path2(icon_dir, "search.png")
        self.filter_le = ButtonLineEdit(icon_path)
        # self.add_btn = QtGui.QToolButton()
        # icon_dir = miraCore.get_icons_dir()
        # self.add_btn.setIcon(QtGui.QIcon(join_path.join_path2(icon_dir, "add.png")))
        horizon_layout.addWidget(self.filter_le)
        # horizon_layout.addWidget(self.add_btn)
        self.list_view = ListView()
        group_layout.addLayout(horizon_layout)
        group_layout.addWidget(self.list_view)
        self.group_box.setLayout(group_layout)
        self.set_model()
        # self.set_signals()

    def set_model(self):
        self.list_model = ListModel(self.model_data)
        self.proxy_model = QtGui.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.list_model)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxy_model.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.list_view.setModel(self.proxy_model)
        self.filter_le.textChanged.connect(self.proxy_model.setFilterRegExp)

    def set_signals(self):
        self.add_btn.clicked.connect(self.add)

    def add(self):
        items_data = self.list_view.get_items_data()
        text = QtGui.QInputDialog.getText(None, "Input the content you want to add", "Content:")
        if text[1]:
            if text[0]:
                if text[0] in items_data:
                    QtGui.QMessageBox.warning(self, "Warning", "Name Warning:%s has been existed in this project." % text[0])
                    return
                if "_" in text[0] or "-" in text[0]:
                    QtGui.QMessageBox.critical(self, "Error", "Name Error:'-' or '_' error.")
                    return
                if not re.match("c\d{3}", text[0]) and not re.match("s\d{3}", text[0]) and re.search("\d+$", text[0]):
                    QtGui.QMessageBox.critical(self, "Error", "Name Error: Asset name con not endswith number.")
                    return
                self.list_model.insertRows(0, 1, text[0])
                row = self.list_model.model_data.index(text[0])
                index = self.list_model.index(row, 0)
                self.list_view.setCurrentIndex(index)
                self.add_signal.emit(text[0])

    def set_group_name(self, value):
        self.group_box.setTitle(value)

    def set_model_data(self, value):
        self.model_data = value
        self.set_model()

    def set_enable(self, value):
        if not value:
            self.filter_le.setEnabled(False)
            self.add_btn.setEnabled(False)
            self.list_view.setEnabled(False)
            self.list_view.clear()
        else:
            self.filter_le.setEnabled(True)
            self.add_btn.setEnabled(True)
            self.list_view.setEnabled(True)


class TaskManagerUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TaskManagerUI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(950, 700)
        self.setWindowTitle("Task Manager")

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(3, 3, 3, 3)

        project_layout = QtGui.QHBoxLayout()
        project_label = QtGui.QLabel("Project")
        project_label.setFixedWidth(70)
        self.project_cbox = QtGui.QComboBox()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        style_layout = QtGui.QHBoxLayout()
        style_label = QtGui.QLabel("Asset/Shot")
        style_label.setFixedWidth(70)
        self.btn_grp = QtGui.QButtonGroup()
        self.asset_check = QtGui.QCheckBox("Asset")
        self.shot_check = QtGui.QCheckBox("Shot")
        self.btn_grp.addButton(self.asset_check)
        self.btn_grp.addButton(self.shot_check)
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.asset_check)
        style_layout.addWidget(self.shot_check)
        style_layout.addStretch()

        engine_layout = QtGui.QHBoxLayout()
        engine_label = QtGui.QLabel("Engine")
        engine_label.setFixedWidth(70)
        engine_layout.addWidget(engine_label)
        self.engine_btn_grp = QtGui.QButtonGroup()
        for engine in ENGINELIST:
            self.engine_check_box = QtGui.QCheckBox(engine)
            if engine == "maya":
                self.engine_check_box.setChecked(True)
            self.engine_btn_grp.addButton(self.engine_check_box)
            engine_layout.addWidget(self.engine_check_box)
        engine_layout.addStretch()

        list_layout = QtGui.QHBoxLayout()
        list_layout.setContentsMargins(0, 3, 0, 3)
        self.first_widget = CommonWidget()
        self.second_widget = CommonWidget()
        self.third_widget = CommonWidget()
        self.third_widget.set_group_name("Step")
        self.fourth_widget = CommonWidget()
        self.fourth_widget.set_group_name("Task")
        list_layout.addWidget(self.first_widget)
        list_layout.addWidget(self.second_widget)
        list_layout.addWidget(self.third_widget)
        list_layout.addWidget(self.fourth_widget)

        separator_layout = QtGui.QHBoxLayout()
        separator_layout.setContentsMargins(0, 10, 0, 0)
        separator_layout.setAlignment(QtCore.Qt.AlignBottom)
        frame = QtGui.QFrame()
        frame.setFrameStyle(QtGui.QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111; width: 10px}')
        separator_layout.addWidget(frame)

        bottom_layout = QtGui.QHBoxLayout()
        bottom_layout.setContentsMargins(0, 3, 0, 3)
        self.user_widget = CommonWidget()
        # self.user_widget.add_btn.setEnabled(False)
        self.user_widget.set_group_name("User")
        self.user_widget.list_view.setSelectionMode(QtGui.QListView.ExtendedSelection)

        start_group = QtGui.QGroupBox("Start date")
        start_layout = QtGui.QHBoxLayout(start_group)
        self.start_widget = QtGui.QCalendarWidget()
        start_layout.addWidget(self.start_widget)

        due_group = QtGui.QGroupBox("Due date")
        due_layout = QtGui.QHBoxLayout(due_group)
        self.due_widget = QtGui.QCalendarWidget()
        due_layout.addWidget(self.due_widget)

        setting_group = QtGui.QGroupBox("Settings")
        setting_layout = QtGui.QGridLayout(setting_group)
        priority_label = QtGui.QLabel("Priority")
        self.priority_cbox = QtGui.QComboBox()
        description_label = QtGui.QLabel("Description")
        description_label.setAlignment(QtCore.Qt.AlignTop)
        self.description_text_edit = QtGui.QTextEdit()
        setting_layout.addWidget(priority_label, 0, 0)
        setting_layout.addWidget(self.priority_cbox, 0, 1)
        setting_layout.addWidget(description_label, 1, 0)
        setting_layout.addWidget(self.description_text_edit, 1, 1)

        bottom_layout.addWidget(self.user_widget)
        bottom_layout.addWidget(start_group)
        bottom_layout.addWidget(due_group)
        bottom_layout.addWidget(setting_group)

        path_layout = QtGui.QHBoxLayout()
        path_label = QtGui.QLabel("Path:")
        path_label.setFixedWidth(30)
        self.path_le = QtGui.QLineEdit()
        self.path_le.setReadOnly(True)
        self.path_btn = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon))
        self.path_btn.setIcon(icon)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_le)
        path_layout.addWidget(self.path_btn)

        button_layout = QtGui.QHBoxLayout()
        self.publish_task_btn = QtGui.QPushButton("Create Task")
        self.cancel_btn = QtGui.QPushButton("Cancel")
        button_layout.addWidget(self.publish_task_btn)
        button_layout.addWidget(self.cancel_btn)

        path_btn_layout = QtGui.QHBoxLayout()
        path_btn_layout.setContentsMargins(0, 0, 0, 0)
        path_btn_layout.addLayout(path_layout)
        path_btn_layout.addLayout(button_layout)

        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 10)
        self.progress_bar.hide()

        main_layout.addLayout(project_layout)
        main_layout.addLayout(style_layout)
        main_layout.addLayout(engine_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(separator_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.addLayout(path_btn_layout)
        main_layout.addWidget(self.progress_bar)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    tm = TaskManagerUI()
    tm.show()
    app.exec_()
