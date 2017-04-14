# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
from task_common_form import CommonForm
from miraLibs.pipeLibs import pipeMira
from miraLibs.pyLibs import Path


class TaskPublish(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TaskPublish, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Task Publish")
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.common_widget = CommonForm()
        bottom_layout = QtGui.QHBoxLayout()
        self.path_le = QtGui.QLineEdit()
        self.path_btn = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon))
        self.path_btn.setIcon(icon)
        self.publish_btn = QtGui.QPushButton("Publish")
        bottom_layout.addWidget(self.path_le)
        bottom_layout.addWidget(self.path_btn)

        main_layout.addWidget(self.common_widget)
        main_layout.addLayout(bottom_layout)
        self.set_signals()

    def set_signals(self):
        self.common_widget.fourth_widget.list_view.clicked.connect(self.show_path)
        self.path_btn.clicked.connect(self.open_dir)

    def show_path(self):
        project = self.common_widget.project
        engine = self.common_widget.engine
        primary = self.common_widget.primary
        engine = self.common_widget.engine
        entity_type = self.common_widget.entity_btn_grp.checkedButton().text()
        first_selected = self.common_widget.first_widget.list_view.get_selected()
        second_selected = self.common_widget.second_widget.list_view.get_selected()
        third_selected = self.common_widget.third_widget.list_view.get_selected()
        fourth_selected = self.common_widget.fourth_widget.list_view.get_selected()
        if not all((first_selected, second_selected, third_selected, fourth_selected)):
            return
        if entity_type == "Asset":
            template = pipeMira.get_site_value(project, "%s_asset_work" % engine)
            file_path = template.format(primary=primary, project=project, asset_type=first_selected[0],
                                        asset_name=second_selected[0].split("_")[-1], step=third_selected[0],
                                        task=fourth_selected[0], version="000", engine=engine)
        else:
            template = pipeMira.get_site_value(project, "%s_shot_work" % engine)
            file_path = template.format(primary=primary, project=project, sequence=first_selected[0],
                                        shot=second_selected[0].split("_")[-1], step=third_selected[0],
                                        task=fourth_selected[0], version="000", engine=engine)
            print file_path
        self.path_le.setText(file_path)

    def open_dir(self):
        path = self.path_le.text()
        if path:
            p = Path.Path(path)
            dir_name = Path.Path(p.dirname())
            dir_name.startfile()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    tm = TaskPublish()
    tm.show()
    app.exec_()
