import glob
import os
from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *
import miraCore
from miraFramework.task_form import my_task_form
from miraLibs.dccLibs import FileOpener
from miraLibs.dccLibs import get_engine
from miraLibs.pyLibs import start_file


class FileListWidget(QListWidget):
    def __init__(self, name=None, parent=None):
        super(FileListWidget, self).__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.name = name
        self.__engine = get_engine.get_engine()
        self.menu = QMenu(self)
        self.open_action = QAction("Open", self)
        self.copy_to_local_action = QAction("Receive The Task", self)
        self.show_in_filesystem_action = QAction("Show in File System", self)
        self.set_signals()
        self.set_style()

    def set_signals(self):
        self.open_action.triggered.connect(self.do_open)
        self.show_in_filesystem_action.triggered.connect(self.show_in_filesystem)

    def contextMenuEvent(self, event):
        self.menu.clear()
        self.menu.addAction(self.open_action)
        self.menu.addAction(self.show_in_filesystem_action)
        if self.name == "work":
            self.menu.addAction(self.copy_to_local_action)
        self.menu.exec_(QCursor.pos())
        event.accept()

    def get_selected(self):
        paths = [item.file_path for item in self.selectedItems()]
        return paths

    def do_open(self):
        file_paths = self.get_selected()
        if not file_paths:
            return
        file_path = file_paths[0]
        fo = FileOpener.FileOpener(file_path)
        fo.run()

    def show_in_filesystem(self):
        file_paths = self.get_selected()
        if not file_paths:
            return
        file_path = file_paths[0]
        if os.path.isfile(file_path):
            dir_name = os.path.dirname(file_path)
        elif os.path.isdir(file_path):
            dir_name = file_path
        start_file.start_file(dir_name)

    def set_style(self):
        style_sheet = "QListWidget::item:selected {background: #29475a;}" \
                      "QListView::item:hover {color: #ff8c00;}"
        self.setStyleSheet(style_sheet)

    def mousePressEvent(self, event):
        pos = event.pos()
        item = self.itemAt(pos)
        if not item:
            self.clearSelection()
        super(FileListWidget, self).mousePressEvent(event)


class StackedWidget(QStackedWidget):
    def __init__(self, name=None, parent=None):
        super(StackedWidget, self).__init__(parent)
        self.resize(375, 500)
        self.name = name
        label = QLabel()
        label.resize(self.width(), self.height())
        icon_path = os.path.abspath(os.path.join(__file__, "..", "no_file.png"))
        pix_map = QPixmap(icon_path)
        pix_map = pix_map.scaled(label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pix_map)
        self.list_widget = FileListWidget(self.name)
        self.addWidget(label)
        self.addWidget(self.list_widget)
    
    def get_engine_icon_path(self, engine):
        icons_dir = miraCore.icons_dir
        engine_icon_path = "%s/%s/%s" % (icons_dir, "engine", "%s.png" % engine)
        return engine_icon_path
        
    def set_dir(self, file_dir):
        self.list_widget.clear()
        engine = os.path.basename(file_dir)
        icon_path = self.get_engine_icon_path(engine)
        if engine == "maya":
            maya_mb_files = glob.glob("%s/*.mb" % file_dir)
            maya_ma_files = glob.glob("%s/*.ma" % file_dir)
            files = maya_mb_files + maya_ma_files
        elif engine == "nuke":
            files = glob.glob("%s/*.nk" % file_dir)
        files.sort()
        files.reverse()
        if files:
            self.setCurrentIndex(1)
            for f in files:
                base_name = os.path.basename(f)
                item = QListWidgetItem(base_name)
                item.setSizeHint(QSize(self.width(), 30))
                item.file_path = f
                item.setIcon(QIcon(icon_path))
                self.list_widget.addItem(item)
        else:
            self.setCurrentIndex(0)


class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)
        self.setColumnCount(3)
        self.setRowCount(0)
        self.setFocusPolicy(Qt.NoFocus)
        self.verticalHeader().setVisible(False)
        self.setHorizontalHeaderLabels(["Step", "Task", "Status"])
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.horizontalHeader().setStretchLastSection(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def append_row(self, step, task, status, status_color):
        row_count = self.rowCount()
        self.setRowCount(row_count + 1)
        step_item = QTableWidgetItem(step)
        step_item.setTextAlignment(Qt.AlignCenter)
        task_item = QTableWidgetItem(task)
        task_item.setTextAlignment(Qt.AlignCenter)
        status_item = QTableWidgetItem(status)
        font = QFont()
        font.setWeight(QFont.Bold)
        status_item.setFont(font)
        status_item.setTextAlignment(Qt.AlignCenter)
        status_item.setForeground(QColor(status_color))
        self.setItem(row_count, 0, step_item)
        self.setItem(row_count, 1, task_item)
        self.setItem(row_count, 2, status_item)


class TaskUI(QDialog):
    def __init__(self, parent=None):
        super(TaskUI, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Task Initialize")
        self.resize(750, 630)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_splitter = QSplitter(Qt.Horizontal)
        self.my_task_widget = my_task_form.MyTaskForm()
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.up_step_table = TableWidget()
        self.up_step_table.setMaximumHeight(85)

        init_layout = QHBoxLayout()
        init_layout.setContentsMargins(0, 0, 0, 0)
        self.init_btn = QPushButton("+ Initialize Task")
        self.init_btn.setStyleSheet("QPushButton{color: #00b4ff; font-size: 10pt; font-weight: bold;}"
                                    "QPushButton:hover{color:#ff8c00}")
        init_layout.addStretch()
        init_layout.addWidget(self.init_btn)

        self.file_widget = QTabWidget()
        self.local_stack = StackedWidget("local")
        self.work_stack = StackedWidget("work")
        self.publish_stack = StackedWidget("publish")
        self.file_widget.addTab(self.local_stack, "Local")
        self.file_widget.addTab(self.work_stack, "Work")
        self.file_widget.addTab(self.publish_stack, "Publish")

        right_layout.addWidget(self.up_step_table)
        right_layout.addLayout(init_layout)
        right_layout.addWidget(self.file_widget)

        main_splitter.addWidget(self.my_task_widget)
        main_splitter.addWidget(right_widget)

        main_splitter.setSizes([self.width()*0.5, self.width()*0.5])
        main_splitter.setStretchFactor(1, 1)

        main_layout.addWidget(main_splitter)


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(TaskUI)
