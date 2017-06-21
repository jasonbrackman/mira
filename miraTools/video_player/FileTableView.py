# -*- coding: utf-8 -*-
import re
import sys
import functools
import tempfile
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from utility.get_icon_dir import get_icon_dir
from utility.get_children_files import get_children_files
from utility.get_conf_data import get_ffmpeg_path, get_valid_ext
from utility.FileMultiThread import FileMultiThread
from ToolWidget import ToolWidget


class FileTableModel(QAbstractTableModel):
    def __init__(self, arg=[[]], parent=None):
        super(FileTableModel, self).__init__(parent)
        self.arg = arg

    def rowCount(self, parent=QModelIndex()):
        return len(self.arg)

    def columnCount(self, parent=QModelIndex()):
        return len(self.arg[0])

    def data(self, index, role=Qt.ToolTipRole):
        if role == Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            return self.arg[row][column]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def setData(self, index, value, role):
        if role == Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            if value:
                self.arg[row][column] = value
                self.dataChanged.emit(index, index)
            return True
        return False

    def insertColumns(self, position, columns, value, parent=QModelIndex()):
        rows = self.rowCount()
        self.beginInsertColumns(parent, position, position+columns-1)
        for row in xrange(rows):
            for index, i in enumerate(value):
                self.arg[row].insert(position+index, i)
        self.endInsertColumns()
        return True

    def removeColumns(self, position, columns, parent=QModelIndex()):
        rows = self.rowCount()
        self.beginRemoveRows(parent, position, position+columns-1)
        for row in xrange(rows):
            for column in xrange(columns):
                for index, value in enumerate(self.arg[row]):
                    if index == position:
                        self.arg[row].remove(value)
        self.endRemoveColumns()
        return True


class FileTableDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(FileTableDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        file_widget = FileWidget(parent)
        return file_widget

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ToolTipRole)
        if value:
            editor.set_file_name(value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class FileWidget(QWidget):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)
        self.__threads = list()
        self.file_name = None
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(100, 56)
        self.icon_label.setStyleSheet("QLabel{background: #000000;}")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.text_label = QLabel()
        self.text_label.setFixedWidth(self.icon_label.width())
        self.text_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.text_label)
        self.show_in_view()

    def show_in_view(self):
        self.set_icon_label()
        if self.file_name:
            self.set_text_label()
            self.show_video_thumbnail()

    def set_file_name(self, value):
        self.file_name = value
        self.show_in_view()

    def set_icon_label(self, icon_path=None):
        icon_dir = get_icon_dir()
        if not icon_path:
            icon_path = os.path.join(icon_dir, "video.png")
        icon_path = icon_path.replace("\\", "/")
        pixmap = QPixmap(icon_path)
        label_width = self.icon_label.width()
        label_height = self.icon_label.height()
        image_width = pixmap.width()
        image_height = pixmap.height()
        if image_width > image_height:
            scaled = pixmap.scaled(QSize(label_width, image_width/label_width*image_height),
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            scaled = pixmap.scaled(QSize(label_height/label_height*image_width, label_height),
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled)

    def set_text_label(self):
        prefix, ext = os.path.splitext(self.file_name)
        base_name = os.path.basename(prefix)
        pattern = ".*_(s.*)_(c.*)_\w+_v\d+"
        matched = re.match(pattern, base_name)
        if matched:
            base_name = "%s_%s" % (matched.group(1), matched.group(2))
        elided_font = QFontMetrics(self.text_label.font())
        text = elided_font.elidedText(base_name, Qt.ElideMiddle, self.text_label.width())
        self.text_label.setText(text)
        self.text_label.setAlignment(Qt.AlignCenter)

    def show_video_thumbnail(self):
        if not os.path.isfile(self.file_name):
            print "%s is not an exist file" % self.file_name
            return
        ffmpeg_path = get_ffmpeg_path()
        temp_path = tempfile.mktemp(suffix=".png", prefix="video_")
        cmd = "%s -ss 00:00:00 -i %s -frames:v 1 %s" % (ffmpeg_path, self.file_name, temp_path)
        thread = FileMultiThread(cmd)
        thread.thread_finished.connect(functools.partial(self.set_icon_label, temp_path))
        thread.start()
        self.__threads.append(thread)
        return temp_path


class FileTableView(QWidget):
    data_changed = Signal()

    def __init__(self, parent=None):
        super(FileTableView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.model_data = [[]]
        self.valid_ext = get_valid_ext()
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        group_box = QGroupBox()
        main_layout.addWidget(group_box)
        group_layout = QVBoxLayout(group_box)
        group_layout.setSpacing(0)
        group_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_widget = ToolWidget(self)
        self.table_view = QTableView()
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().hide()
        self.table_view.setSelectionMode(QListWidget.ExtendedSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.remove_action = QAction("remove", self)
        self.add_action = QAction("add", self)
        self.table_view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.table_view.addAction(self.remove_action)
        self.table_view.addAction(self.add_action)
        group_layout.addWidget(self.tool_widget)
        group_layout.addWidget(self.table_view)
        self.resize(500, 80)
        self.set_signals()

    def set_signals(self):
        self.tool_widget.add_btn.clicked.connect(self.on_add_btn_clicked)
        self.tool_widget.remove_btn.clicked.connect(self.remove_column)
        self.tool_widget.insert_btn.clicked.connect(self.on_insert_btn_clicked)
        self.tool_widget.clear_btn.clicked.connect(self.on_clear_btn_clicked)
        self.remove_action.triggered.connect(self.remove_column)
        self.add_action.triggered.connect(self.insert_column)

    def set_model(self):
        self.model = FileTableModel(self.model_data, self)
        self.table_view.setModel(self.model)
        self.set_delegate()
        self.data_changed.emit()

    def set_delegate(self):
        delegate = FileTableDelegate(self.table_view)
        self.table_view.setItemDelegateForRow(0, delegate)
        for i in xrange(self.model.columnCount()):
            self.table_view.openPersistentEditor(self.model.index(0, i))

    def set_table_view(self, model_data):
        """
        :param model_data: a file list.
        :return:
        """
        if not model_data:
            return
        self.on_clear_btn_clicked()
        if not isinstance(model_data[0], list):
            self.model_data = [model_data]
        self.set_model()
        self.table_view.resizeRowsToContents()
        self.table_view.resizeColumnsToContents()

    def get_selected_columns(self):
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            return
        columns = list()
        for index in selected_indexes:
            columns.append(index.column())
        return columns

    def remove_column(self):
        selected_columns = self.get_selected_columns()
        if not selected_columns:
            return
        if not self.model_data[0]:
            return
        for index, column in enumerate(selected_columns):
            for data_index, value in enumerate(self.model_data[0]):
                if data_index == column-index:
                    self.model_data[0].remove(value)
        self.set_model()

    def insert_column(self, value):
        """
        :param value: a file list need to insert
        :return:
        """
        if not value:
            print "No video insert."
            return
        selected_columns = self.get_selected_columns()
        if not selected_columns:
            return
        if isinstance(value, basestring):
            value = [value]
        value = [i for i in value if i not in self.model_data[0]]
        position = selected_columns[0] + 1
        for index, i in enumerate(value):
            self.model_data[0].insert(position+index, i)
        self.set_model()

    def add_column(self, value):
        """
        :param value: a file list
        :return:
        """
        if not value:
            return
        value = [i.replace("\\", "/")for i in value]
        if not self.model_data[0]:
            self.set_table_view(value)
        else:
            value = [i for i in value if i not in self.model_data[0]]
            if not value:
                return
            column_count = len(self.model_data[0])
            position = column_count + 1
            for index, i in enumerate(value):
                self.model_data[0].insert(position+index, i)
            self.set_model()

    def on_add_btn_clicked(self):
        file_list = QFileDialog.getOpenFileNames(self, "choose directory", "",
                                                       "video files(%s)" % (" *"+" *".join(self.valid_ext)))
        if not file_list[0]:
            return
        file_list = [f.replace("\\", "/") for f in file_list[0]]
        if not self.model_data[0]:
            self.set_table_view(file_list)
        else:
            self.add_column(file_list)

    def on_insert_btn_clicked(self):
        file_list = QFileDialog.getOpenFileNames(self, "choose directory", "",
                                                       "video files(%s)" % (" *"+" *".join(self.valid_ext)))
        if not file_list[0]:
            return
        file_list = [f.replace("\\", "/") for f in file_list[0]]
        self.insert_column(file_list)

    def on_clear_btn_clicked(self):
        if self.model_data[0]:
            self.model.removeColumns(0, len(self.model_data[0]))
            self.model_data = [[]]
            self.data_changed.emit()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = list()
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            children_files = get_children_files(path, self.valid_ext)
            files.extend(children_files)
        files.sort()
        need_added = [f for f in files if f not in self.model_data[0]]
        self.add_column(need_added)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.remove_column()
