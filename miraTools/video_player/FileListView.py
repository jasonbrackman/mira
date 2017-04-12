# -*- coding: utf-8 -*-
import sys
import functools
import tempfile
import os
from PySide import QtGui, QtCore
from utility.get_icon_dir import get_icon_dir
from utility.get_conf_data import get_ffmpeg_path, get_valid_ext
from utility.FileMultiThread import FileMultiThread
from ToolWidget import ToolWidget


class FileListModel(QtCore.QAbstractListModel):
    def __init__(self, arg=[], parent=None):
        super(FileListModel, self).__init__(parent)
        self.arg = arg

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.arg)

    def data(self, index, role=QtCore.Qt.ToolTipRole):
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            return self.arg[row]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for index, i in enumerate(value):
            self.arg.insert(position+index, i)
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.arg[position]
            self.arg.remove(value)
        self.endRemoveRows()
        return True


class FileListDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        super(FileListDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        file_widget = FileWidget(parent)
        return file_widget

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.ToolTipRole)
        if value:
            editor.set_file_name(value)

    def sizeHint(self, option, index):
        return QtCore.QSize(200, 64)


class FileWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)
        self.__threads = list()
        # self.setFrameStyle(QtGui.QFrame.Raised | QtGui.QFrame.Box)
        self.file_name = None
        main_layout = QtGui.QHBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        main_layout.setContentsMargins(0, 2, 0, 1)
        text_label_layout = QtGui.QVBoxLayout()
        text_label_layout.setContentsMargins(6, 0, 0, 0)
        self.icon_label = QtGui.QLabel()
        self.icon_label.setFixedSize(100, 56)
        self.icon_label.setStyleSheet("QLabel{background: #000000;}")
        self.icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label = QtGui.QLabel()
        self.text_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        text_label_layout.addWidget(self.text_label)
        main_layout.addWidget(self.icon_label)
        main_layout.addLayout(text_label_layout)
        self.show_in_view()

    def show_in_view(self):
        self.set_icon_label()
        if self.file_name:
            self.set_text_label()
            self.show_video_thumbnail()

    def set_file_name(self, value):
        """
        access to outer
        :param value:
        :return:
        """
        self.file_name = value
        self.show_in_view()

    def set_icon_label(self, icon_path=None):
        icon_dir = get_icon_dir()
        if not icon_path:
            icon_path = os.path.join(icon_dir, "video.png")
        icon_path = icon_path.replace("\\", "/")
        pixmap = QtGui.QPixmap(icon_path)
        label_width = self.icon_label.width()
        label_height = self.icon_label.height()
        image_width = pixmap.width()
        image_height = pixmap.height()
        if image_width > image_height:
            scaled = pixmap.scaled(QtCore.QSize(label_width, image_width/label_width*image_height),
                                   QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        else:
            scaled = pixmap.scaled(QtCore.QSize(label_height/label_height*image_width, label_height),
                                   QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled)

    def set_text_label(self):
        if "</font>" in self.file_name:
            base_name = self.file_name
        else:
            base_name = os.path.basename(self.file_name)
        elided_font = QtGui.QFontMetrics(self.text_label.font())
        text = elided_font.elidedText(base_name, QtCore.Qt.ElideMiddle, self.text_label.width())
        self.text_label.setText(text)

    def show_video_thumbnail(self):
        if not os.path.isfile(self.file_name) or os.path.isdir(self.file_name):
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


class FileListView(QtGui.QWidget):
    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)
        self.model = FileListModel([], self)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        group_box = QtGui.QGroupBox()
        main_layout.addWidget(group_box)
        group_layout = QtGui.QVBoxLayout(group_box)
        group_layout.setSpacing(0)
        group_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_widget = ToolWidget(self)
        self.list_view = QtGui.QListView()
        self.list_view.setSelectionMode(QtGui.QListWidget.ExtendedSelection)
        self.list_view.setModel(self.model)
        self.setAcceptDrops(True)
        group_layout.addWidget(self.tool_widget)
        group_layout.addWidget(self.list_view)
        self.set_signals()

    def set_signals(self):
        self.tool_widget.add_btn.clicked.connect(self.on_add_btn_clicked)
        self.tool_widget.remove_btn.clicked.connect(self.remove_row)
        self.tool_widget.insert_btn.clicked.connect(self.on_insert_btn_clicked)
        self.tool_widget.clear_btn.clicked.connect(self.on_clear_btn_clicked)
        self.model.rowsInserted.connect(self.set_delegate)
        self.model.rowsRemoved.connect(self.set_delegate)

    def set_delegate(self):
        self.delegate = FileListDelegate(self.list_view)
        self.list_view.setItemDelegate(self.delegate)
        for i in xrange(self.model.rowCount()):
            self.list_view.openPersistentEditor(self.model.index(i, 0))

    def set_list_view(self, model_data):
        # self.on_clear_btn_clicked()
        if isinstance(model_data, basestring):
            model_data = model_data.replace("\\", "/")
            model_data = [model_data]
        if not model_data:
            return
        model_data = [i.replace("\\", "/") for i in model_data]
        self.add_row(model_data)

    def get_selected_rows(self):
        selected_indexes = self.list_view.selectedIndexes()
        if not selected_indexes:
            return
        rows = list()
        for index in selected_indexes:
            rows.append(index.row())
        return rows

    def insert_row(self, value):
        """
        :param value: a file list need to insert
        :return:
        """
        if not value:
            print "No video insert."
            return
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            return
        position = selected_rows[0]
        if isinstance(value, basestring):
            value = [value]
        self.model.insertRows(position, len(value), value)

    def add_row(self, value):
        # if value in self.model.arg:
        #     return
        if isinstance(value, basestring):
            value = [value]
        self.model.insertRows(self.model.rowCount(), len(value), value)

    def remove_row(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            return
        selected_rows.sort()
        for index, row in enumerate(selected_rows):
            self.model.removeRows(row-index, 1)

    def on_add_btn_clicked(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "choose directory")
        if not directory:
            return
        directory = directory.replace("\\", "/")
        if self.model.arg:
            self.add_row(directory)
        else:
            self.set_list_view(directory)

    def on_insert_btn_clicked(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "choose directory")
        if not directory:
            return
        directory = directory.replace("\\", "/")
        self.insert_row(directory)

    def on_clear_btn_clicked(self):
        row_count = self.model.rowCount()
        if row_count:
            self.model.removeRows(0, row_count)

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
        valid_ext = get_valid_ext()
        files = list()
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            path = path.replace("\\", "/")
            if os.path.isfile(path) and os.path.splitext(path)[-1] in valid_ext:
                files.append(path)
            if os.path.isdir(path):
                files.append(path)
        files.sort()
        need_added = [f for f in files if f not in self.model.arg]
        self.add_row(need_added)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.remove_row()
