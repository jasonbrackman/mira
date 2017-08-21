import os
import glob
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from miraFramework.task_form import my_task_form
from miraLibs.osLibs import get_engine


class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent)
        self.__engine = get_engine.get_engine()

    def set_dir(self, file_dir):
        self.clear()
        if self.__engine == "maya":
            maya_mb_files = glob.glob("%s/*.mb" % (file_dir))
            maya_ma_files = glob.glob("%s/*.ma" % (file_dir))
            files = maya_mb_files + maya_ma_files
            files.sort()
        if not files:
            return
        for f in files:
            base_name = os.path.basename(f)
            item = QListWidgetItem(base_name)
            item.file_path = f
            self.addItem(item)
        

class TaskUI(QDialog):
    def __init__(self, parent=None):
        super(TaskUI, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Task Get")
        self.resize(750, 630)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_splitter = QSplitter(Qt.Horizontal)
        self.my_task_widget = my_task_form.MyTaskForm()
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        task_group = QGroupBox()
        current_task_layout = QHBoxLayout(task_group)
        task_label = QLabel()
        task_label.setText("<font color=#00b4ff size=5>Task:</font>")
        task_label.setMinimumHeight(50)
        task_label.setFixedWidth(50)
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.info_label.setMinimumHeight(50)

        current_task_layout.addWidget(task_label)
        current_task_layout.addWidget(self.info_label)

        init_layout = QHBoxLayout()
        init_layout.setContentsMargins(0, 0, 0, 0)
        self.init_btn = QPushButton("+ Initialize Task")
        self.init_btn.setStyleSheet("color: #00b4ff; font-size: 10pt; font-weight: bold; ")
        init_layout.addStretch()
        init_layout.addWidget(self.init_btn)

        self.file_widget = QTabWidget()
        self.local_list = FileListWidget()
        self.work_list = FileListWidget()
        self.publish_list = FileListWidget()
        self.file_widget.addTab(self.local_list, "Local")
        self.file_widget.addTab(self.work_list, "Work")
        self.file_widget.addTab(self.publish_list, "Publish")

        right_layout.addWidget(task_group)
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
