# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
import miraCore
from miraFramework.Filter import Filter
from miraFramework.combo import ProjectCombo
from miraLibs.pyLibs import join_path
from miraLibs.pipeLibs import pipeMira, get_current_project
from miraLibs.dbLibs import db_api
from miraLibs.pipeLibs import pipeHistory


class ListModel(QAbstractListModel):
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

    def rowCount(self, parent=QModelIndex()):
        return len(self.__model_data)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            return self.__model_data[row]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for i in range(count):
            self.__model_data.insert(position, value)
        self.__model_data.sort()
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.__model_data[position]
            self.__model_data.remove(value)
        self.endRemoveRows()
        return True


class ListView(QListView):
    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)
        self.menu = QMenu()
        self.remove_action = QAction("remove", self)
        self.setSelectionBehavior(QListView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("QListView::item:selected{background: #ff8c00;}")

    def remove_item(self):
        model = self.model()
        if isinstance(model, QSortFilterProxyModel):
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
        if isinstance(model, QSortFilterProxyModel):
            model = model.sourceModel()
        model.model_data = list()
        self.setModel(model)

    def get_items_data(self):
        items_data = list()
        model = self.model()
        if isinstance(model, QSortFilterProxyModel):
            model = model.sourceModel()
        for i in xrange(model.rowCount(self)):
            model_index = model.index(i, 0)
            data = model_index.data()
            # data = self.list_model.data(model_index, Qt.DisplayRole)
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


class CommonWidget(QWidget):
    add_signal = Signal(basestring)

    def __init__(self, parent=None):
        super(CommonWidget, self).__init__(parent)
        self.resize(150, 180)
        self.model_data = list()
        self.group_name = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.group_box = QGroupBox()
        main_layout.addWidget(self.group_box)
        group_layout = QVBoxLayout()

        icon_dir = miraCore.get_icons_dir()
        icon_path = join_path.join_path2(icon_dir, "search.png")
        self.filter_le = Filter(icon_path)

        self.list_view = ListView()
        group_layout.addWidget(self.filter_le)
        group_layout.addWidget(self.list_view)
        self.group_box.setLayout(group_layout)
        self.set_model()
        # self.set_signals()

    def set_model(self):
        self.list_model = ListModel(self.model_data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.list_model)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.list_view.setModel(self.proxy_model)
        self.filter_le.textChanged.connect(self.proxy_model.setFilterRegExp)

    def set_signals(self):
        self.add_btn.clicked.connect(self.add)

    def set_group_name(self, value):
        self.group_box.setTitle(value)

    def set_model_data(self, value):
        if not value:
            return
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


class CommonForm(QWidget):
    def __init__(self, parent=None):
        super(CommonForm, self).__init__(parent)
        self.setup_ui()
        self.init()
        self.set_signals()
        self.db = db_api.DbApi(self.project).db_obj
        self.__asset_types = pipeMira.get_studio_value(self.project, "asset_type")

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(3, 3, 3, 3)

        project_layout = QHBoxLayout()
        project_label = QLabel("Project")
        project_label.setFixedWidth(70)
        self.project_cbox = ProjectCombo()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        entity_type_layout = QHBoxLayout()
        style_label = QLabel("Asset/Shot")
        style_label.setFixedWidth(70)
        self.entity_btn_grp = QButtonGroup()
        self.asset_check = QCheckBox("Asset")
        self.shot_check = QCheckBox("Shot")
        self.entity_btn_grp.addButton(self.asset_check)
        self.entity_btn_grp.addButton(self.shot_check)
        entity_type_layout.addWidget(style_label)
        entity_type_layout.addWidget(self.asset_check)
        entity_type_layout.addWidget(self.shot_check)
        entity_type_layout.addStretch()

        list_layout = QHBoxLayout()
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

        separator_layout = QHBoxLayout()
        separator_layout.setContentsMargins(0, 10, 0, 0)
        separator_layout.setAlignment(Qt.AlignBottom)
        frame = QFrame()
        frame.setFrameStyle(QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111; width: 10px}')
        separator_layout.addWidget(frame)

        main_layout.addLayout(project_layout)
        main_layout.addLayout(entity_type_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(separator_layout)

    @staticmethod
    def get_selected(widget):
        temp = widget.list_view.get_selected()
        result = temp[0] if temp else None
        return result

    @property
    def project(self):
        return self.project_cbox.currentText()

    @property
    def primary(self):
        return pipeMira.get_primary_dir(self.project)

    @property
    def mayabatch(self):
        return pipeMira.get_mayabatch_path(self.project)

    @property
    def entity_type(self):
        return self.entity_btn_grp.checkedButton().text()

    @property
    def asset_type_or_sequence(self):
        return self.get_selected(self.first_widget)

    @property
    def asset_or_shot(self):
        return self.get_selected(self.second_widget)

    @property
    def step(self):
        return self.get_selected(self.third_widget)

    @property
    def task(self):
        return self.get_selected(self.fourth_widget)

    @property
    def task_info(self):
        entity_type = self.entity_type
        asset_type_or_sequence = self.asset_type_or_sequence
        asset_or_shot = self.asset_or_shot
        step = self.step
        task = self.task
        arg_list = (entity_type, asset_type_or_sequence, asset_or_shot, step, task)
        if not all(arg_list):
            return
        return self.db.get_current_task(*arg_list)

    def init(self):
        projects = pipeMira.get_projects()
        self.project_cbox.addItems(projects)
        current_project = get_current_project.get_current_project()
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(current_project))

    def set_signals(self):
        self.project_cbox.currentIndexChanged[str].connect(self.on_project_changed)
        self.entity_btn_grp.buttonClicked.connect(self.init_grp)
        self.first_widget.list_view.clicked.connect(self.show_asset_or_shot)
        self.second_widget.list_view.clicked.connect(self.show_step)
        self.third_widget.list_view.clicked.connect(self.show_task)

    def on_project_changed(self, project):
        pipeHistory.set("currentProject", project)
        self.db = db_api.DbApi(project).db_obj
        self.asset_check.setChecked(False)
        self.shot_check.setChecked(False)
        for widget in [self.first_widget, self.second_widget, self.third_widget, self.fourth_widget]:
            widget.list_view.clear()

    def init_grp(self):
        checked_btn_text = self.entity_btn_grp.checkedButton().text()
        for widget in [self.first_widget, self.second_widget, self.third_widget, self.fourth_widget]:
            widget.list_view.clear()
        if checked_btn_text == "Asset":
            # set group name
            self.first_widget.set_group_name("Asset Type")
            self.second_widget.set_group_name("Asset")
            self.second_widget.list_view.clear()
            # init list view
            self.first_widget.set_model_data(self.__asset_types)
        else:
            self.first_widget.set_group_name("Sequence")
            self.second_widget.set_group_name("Shot")
            self.second_widget.list_view.clear()
            # init list view
            sequences = self.db.get_sequence()
            self.first_widget.set_model_data(sequences)

    def show_asset_or_shot(self, index):
        for widget in [self.second_widget, self.third_widget, self.fourth_widget]:
            widget.list_view.clear()
        selected = index.data()
        if self.entity_type == "Asset":
            assets = self.db.get_all_assets(selected)
            if self.db.typ == "shotgun":
                asset_names = [asset["code"] for asset in assets]
            elif self.db.typ == "strack":
                asset_names = [asset["name"] for asset in assets]
            else:
                return
            self.second_widget.set_model_data(asset_names)
        elif self.entity_type == "Shot":
            shots = self.db.get_all_shots(selected)
            shot_names = [shot["name"] for shot in shots]
            self.second_widget.set_model_data(shot_names)

    def show_step(self, index):
        for widget in [self.third_widget, self.fourth_widget]:
            widget.list_view.clear()
        asset_or_shot = index.data()
        if not self.asset_type_or_sequence:
            return
        steps = self.db.get_step(self.entity_type, self.asset_type_or_sequence, asset_or_shot)
        if not steps:
            print "No step under this entity"
            return
        step_names = list(set(steps))
        self.third_widget.set_model_data(step_names)

    def show_task(self, index):
        self.fourth_widget.list_view.clear()
        step = index.data()
        if not all((self.asset_type_or_sequence, self.asset_or_shot)):
            return
        tasks = self.db.get_task(self.entity_type, self.asset_type_or_sequence, self.asset_or_shot, step)
        if not tasks:
            return
        if self.db.typ == "shotgun":
            task_names = [task["content"] for task in tasks]
        elif self.db.typ == "strack":
            task_names = [task["name"] for task in tasks]
        else:
            return
        self.fourth_widget.set_model_data(task_names)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    cf = CommonForm()
    cf.show()
    app.exec_()
