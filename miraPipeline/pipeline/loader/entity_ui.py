# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import os
from hooks import Hook
from miraFramework.Filter import Filter
from miraFramework.waiting import Waiting
from miraFramework.combo import ProjectCombo
import miraCore
from miraLibs.pipeLibs import pipeMira
from miraLibs.dbLibs import db_api
reload(db_api)
from miraLibs.qtLibs import create_round_rect_thumbnail
from miraLibs.pipeLibs import pipeFile, Step
from miraLibs.pyLibs import join_path, yml_operation
from miraLibs.osLibs import get_engine


IMAGE_WIDTH, IMAGE_HEIGHT = [110, 80]
LIST_VIEW_STYLE = "QListView::item:selected {color: #fff; background: #29475a; " \
                  "border: 1px solid #00b4ff; border-radius: 5px;}" \
                  "QListView::item:hover {color: #ff8c00}"


class ThumbListView(QListView):
    left_pressed = Signal(QModelIndex)

    def __init__(self, parent=None):
        super(ThumbListView, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setFlow(QListView.LeftToRight)
        self.setMovement(QListView.Static)
        self.setFocusPolicy(Qt.NoFocus)
        self.setWrapping(True)
        self.setSpacing(10)
        self.setStyleSheet(LIST_VIEW_STYLE)

    def mousePressEvent(self, event):
        pos = event.pos()
        index = self.indexAt(pos)
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                super(ThumbListView, self).mousePressEvent(event)
            else:
                if index.isValid():
                    self.left_pressed.emit(index)
                    super(ThumbListView, self).mousePressEvent(event)
                else:
                    self.clearSelection()


class EntityUI(QWidget):
    def __init__(self, parent=None):
        super(EntityUI, self).__init__(parent)
        self.setWindowTitle("Loader")
        self.setObjectName("Loader")
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)

        project_layout = QHBoxLayout()
        project_layout.setContentsMargins(0, 0, 0, 0)
        project_label = QLabel("Project")
        project_label.setFixedWidth(50)
        self.project_cbox = ProjectCombo()
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_cbox)

        self.entity_tab = QTabWidget()
        asset_widget = QWidget()
        self.asset_layout = QHBoxLayout(asset_widget)
        self.asset_layout.setAlignment(Qt.AlignTop)
        self.asset_btn_grp = QButtonGroup()
        self.asset_btn_grp.setExclusive(True)
        self.entity_tab.addTab(asset_widget, "Asset")
        self.entity_tab.setMaximumHeight(60)

        shot_widget = QWidget()
        shot_layout = QHBoxLayout(shot_widget)
        sequence_label = QLabel("Sequence")
        sequence_label.setFixedWidth(60)
        self.sequence_le = QLineEdit()
        shot_layout.addWidget(sequence_label)
        shot_layout.addWidget(self.sequence_le)
        self.entity_tab.addTab(shot_widget, "Shot")

        filter_layout = QHBoxLayout()
        self.filter_le = Filter()
        filter_layout.addStretch()
        filter_layout.addWidget(self.filter_le)

        self.list_view = ThumbListView()
        show_layout = QHBoxLayout()
        show_label = QLabel("Current Selected:")
        self.show_le = QLineEdit()
        self.show_le.setReadOnly(True)
        self.show_le.setStyleSheet("border: 0px solid;")
        show_layout.addWidget(show_label)
        show_layout.addWidget(self.show_le)

        main_layout.addLayout(project_layout)
        main_layout.addWidget(self.entity_tab)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.list_view)
        main_layout.addLayout(show_layout)

        self.waiting_widget = Waiting(self.list_view)
        self.waiting_widget.hide()


class RunThread(QThread):
    signal = Signal(list)

    def __init__(self, project, entity_type, asset_type_sequence, entities, parent=None):
        super(RunThread, self).__init__(parent)
        self.__project = project
        self.__asset_type_sequence = asset_type_sequence
        self.__entity_type = entity_type
        self.__entities = entities
        self.__image_dir = miraCore.get_icons_dir()
        self.__collect_data = list()

    def run(self):
        studio_conf_path = join_path.join_path2(miraCore.get_conf_dir(), "studio.yml")
        yml_data = yml_operation.get_yaml_data(studio_conf_path)
        project_data = yml_data.get(self.__project)
        primary = project_data.get("primary")
        if self.__entity_type == "Asset":
            format_str = project_data.get("maya_asset_image")
            step = "MidMdl"
            task = "MidMdl"
        else:
            format_str = project_data.get("maya_shot_image")
            step = "AnimLay"
            task = "AnimLay"
        engine = Step(self.__project, step).engine
        for entity in self.__entities:
            entity_name = entity.get("name")
            image_path = format_str.format(primary=primary, project=self.__project,
                                           asset_type=self.__asset_type_sequence, sequence=self.__asset_type_sequence,
                                           asset_name=entity_name, shot=entity_name.split("_")[-1],
                                           step=step, task=task, engine=engine)

            if self.__entity_type == "Asset" and not os.path.isfile(image_path):
                image_path = format_str.format(primary=primary, project=self.__project,
                                               asset_type=self.__asset_type_sequence,
                                               asset_name=entity_name, step="Group", task="Group", engine=engine)
            if self.__entity_type == "Shot" and not os.path.isfile(image_path):
                image_path = format_str.format(primary=primary, project=self.__project,
                                               sequence=self.__asset_type_sequence,
                                               shot=entity_name.split("_")[-1], step="Set", task="Set", engine=engine)
            if not os.path.isfile(image_path):
                image_path = join_path.join_path2(self.__image_dir, "unknown.png")
            self.__collect_data.append([entity_name, image_path])

        self.signal.emit(self.__collect_data)


class AssetItem(object):
    def __init__(self, project=None, name=None, image=None):
        self.project = project
        self.name = name
        self.image = image


class EntityModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(EntityModel, self).__init__(parent)
        self.model_data = model_data

    def rowCount(self, parent=QModelIndex()):
        return len(self.model_data)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        item = self.model_data[row]
        if role == Qt.DisplayRole:
            name = item.name
            elidfont = QFontMetrics(QFont("Arial", 8, QFont.Bold))
            text = elidfont.elidedText(name, Qt.ElideRight, IMAGE_WIDTH)
            return text
        if role == Qt.FontRole:
            return QFont("Arial", 8, QFont.Bold)
        if role == Qt.ForegroundRole:
            return QColor("#fff")
        if role == Qt.ToolTipRole:
            return item.name
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


class FilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(FilterProxyModel, self).__init__(parent)
        self.name_regexp = QRegExp()
        self.name_regexp.setCaseSensitivity(Qt.CaseInsensitive)
        self.name_regexp.setPatternSyntax(QRegExp.RegExp)

    def filterAcceptsRow(self, source_row, source_parent):
        name_index = self.sourceModel().index(source_row, 0, source_parent)
        item = self.sourceModel().data(name_index, Qt.ToolTipRole)
        if self.name_regexp.isEmpty():
            return True
        else:
            return self.name_regexp.exactMatch(item)

    def set_name_filter(self, regexp):
        regexp = ".*%s.*" % regexp if regexp else ""
        self.name_regexp.setPattern(regexp)
        self.invalidateFilter()


class Entity(EntityUI):
    def __init__(self, parent=None):
        super(Entity, self).__init__(parent)
        self.__init_asset_type()
        self.db = db_api.DbApi(self.project).db_obj
        self.__main_menu = QMenu()
        self.__entity_action_group = QActionGroup(self)
        self.__task_action_group = QActionGroup(self)
        self.__set_signals()
        self.__threads = list()
        self.engine = get_engine.get_engine()

    @property
    def project(self):
        return self.project_cbox.currentText()

    @property
    def asset_type_sequence(self):
        if self.entity_type == "Asset":
            return self.asset_btn_grp.checkedButton().text()
        else:
            return self.sequence_le.text()

    @property
    def entity_type(self):
        tab_index = self.entity_tab.currentIndex()
        if tab_index == 0:
            return "Asset"
        else:
            return "Shot"

    @property
    def pipeline_steps(self):
        if self.entity_type == "Asset":
            return pipeMira.get_studio_value(self.project, "asset_steps")
        else:
            return pipeMira.get_studio_value(self.project, "shot_steps")

    def __init_asset_type(self):
        asset_types = pipeMira.get_studio_value(self.project, "asset_type")
        for asset_type in asset_types:
            self.asset_type_check = QCheckBox(asset_type)
            self.asset_btn_grp.addButton(self.asset_type_check)
            self.asset_layout.addWidget(self.asset_type_check)

    def __init_sequence(self):
        sequences = self.db.get_all_sequences()
        if not sequences:
            return
        sequences.sort()
        completer = QCompleter(sequences)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.sequence_le.setCompleter(completer)

    def __set_signals(self):
        self.asset_btn_grp.buttonClicked.connect(self.__calculate_entities)
        self.__task_action_group.triggered.connect(self.__on_action_triggered)
        self.__entity_action_group.triggered.connect(self.__on_action_triggered)
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)
        self.list_view.clicked.connect(self.show_selected)
        self.entity_tab.currentChanged.connect(self.__switch_entity)
        self.sequence_le.returnPressed.connect(self.__calculate_entities)

    def __switch_entity(self, index):
        if index == 0:
            self.asset_btn_grp.setExclusive(False)
            for btn in self.asset_btn_grp.buttons():
                btn.setChecked(False)
            self.asset_btn_grp.setExclusive(True)
        else:
            self.sequence_le.setText("")
            self.__init_sequence()
        self.__set_empty_model()

    def __set_empty_model(self):
        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)

    def __set_model(self, model_data):
        if not model_data:
            self.__set_empty_model()
            return
        self.proxy_model = FilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model .setSortCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.filter_le.textChanged.connect(self.proxy_model.set_name_filter)
        self.model = EntityModel(model_data)
        self.proxy_model.setSourceModel(self.model)
        self.list_view.setModel(self.proxy_model)

    def __calculate_entities(self):
        self.waiting_widget.show()
        if self.entity_type == "Asset":
            entities = self.db.get_all_assets(self.asset_type_sequence)
        else:
            sequence = self.sequence_le.text()
            entities = self.db.get_all_shots(sequence) if sequence else []
        if not entities:
            self.__set_empty_model()
            self.waiting_widget.hide()
            return
        thread = RunThread(self.project, self.entity_type, self.asset_type_sequence, entities)
        thread.signal.connect(self.__show_entities)
        self.__threads.append(thread)
        thread.start()

    def __show_entities(self, value):
        model_data = list()
        for data in value:
            entity_name, image_path = data
            image = create_round_rect_thumbnail.create_round_rect_thumbnail(image_path, IMAGE_WIDTH, IMAGE_HEIGHT, 10)
            item = AssetItem(self.project, entity_name, image)
            model_data.append(item)
        self.__set_model(model_data)
        self.waiting_widget.quit()

    def __get_selected(self):
        selected_indexes = self.list_view.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = [self.proxy_model.mapToSource(index).row() for index in selected_indexes]
        selected_rows = list(set(selected_rows))
        selected = [self.model.model_data[row] for row in selected_rows]
        return selected

    def get_actions(self):
        conf_path = os.path.abspath(os.path.join(__file__, "..", "conf.yml")).replace("\\", "/")
        conf_data = yml_operation.get_yaml_data(conf_path)
        if self.engine in conf_data:
            return conf_data[self.engine]
        else:
            print "conf.yml not include current engine" % self.engine
            return

    def show_context_menu(self, pos):
        # add entity menu and action
        self.__main_menu.clear()
        actions = self.get_actions().get(self.entity_type)
        if not actions:
            return
        entity_actions = actions.get("entity").get("actions")
        task_actions = actions.get("task").get("actions")
        selected = self.__get_selected()
        if not selected:
            return
        asset_shot_names = [item.name for item in selected]
        out_arg = [self.project, self.entity_type, self.asset_type_sequence, asset_shot_names]
        for action in entity_actions:
            entity_action = self.__entity_action_group.addAction(action)
            entity_action.attr = out_arg
            self.__main_menu.addAction(entity_action)
        if not task_actions:
            return
        # add task menu and action
        if len(selected) > 1:
            if self.entity_type == "Asset":
                steps = pipeMira.get_studio_value(self.project, "asset_steps")
            else:
                steps = pipeMira.get_studio_value(self.project, "shot_steps")
        if len(selected) == 1:
            steps = self.db.get_step(self.entity_type, self.asset_type_sequence, asset_shot_names[0])
            if not steps:
                return
            steps = list(set(steps))
            steps.sort()
        for step in steps:
            step_menu = self.__main_menu.addMenu(step)
            step_menu.up_level = self.__main_menu
            if len(selected) == 1:
                tasks = self.db.get_task(self.entity_type, self.asset_type_sequence, asset_shot_names[0], step)
                tasks = [task.get("name") for task in tasks]
            else:
                tasks = [step]
            if not tasks:
                continue
            for task in tasks:
                task_menu = step_menu.addMenu(task)
                task_menu.up_level = step_menu
                for action in task_actions:
                    task_action = self.__task_action_group.addAction(action)
                    task_action.up_level = task_menu
                    task_action.attr = out_arg
                    task_menu.addAction(task_action)
        global_pos = self.list_view.mapToGlobal(pos)
        self.__main_menu.exec_(global_pos)

    def __get_publish_path(self, entity_type, typ, name, step, task):
        publish_file_path = pipeFile.get_task_publish_file(self.project, entity_type, typ, name, step, task)
        return publish_file_path

    def __on_action_triggered(self, action):
        project, entity_type, asset_type_sequence, asset_shot_names = action.attr
        if hasattr(action, "up_level"):
            task = action.up_level.title()
            step = action.up_level.up_level.title()
        else:
            task = None
            step = None
        action_name = action.text()
        hooker = Hook(project, entity_type, asset_type_sequence, asset_shot_names, step, task, action_name)
        hooker.execute()

    def show_selected(self, index):
        source_index = self.proxy_model.mapToSource(index)
        selected_item = self.model.model_data[source_index.row()]
        selected = selected_item.name
        self.show_le.setText(selected)

    def resizeEvent(self, event):
        self.waiting_widget.resize(event.size())
        event.accept()


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(Entity)
