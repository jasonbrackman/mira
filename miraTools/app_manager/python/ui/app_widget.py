# -*- coding: utf-8 -*-
import os
from PySide import QtGui, QtCore
from . import app_cell_widget
from ..libs import get_conf_path, conf_parser
from ..frameworks.separator import Separator


class AppWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AppWidget, self).__init__(parent)
        self.separators = list()
        self.setup_ui()
        self.init()

    def setup_ui(self):
        self.app_layout = QtGui.QVBoxLayout(self)
        self.app_layout.setAlignment(QtCore.Qt.AlignTop)
        self.app_layout.setContentsMargins(0, 0, 0, 0)

    def insert_cell_widget(self, name, collapse, index):
        true_index = (index-1)*2
        cell_widgets = self.get_all_cell_widget()
        cell_widget_names = [widget.name for widget in cell_widgets]
        name = name.upper()
        if name in cell_widget_names:
            return
        cell_widget = app_cell_widget.AppCellWidget(name, collapse, self)
        cell_widget.delete_signal.connect(self.delete_separator)
        sep = Separator()
        sep.widget_name = name
        self.separators.append(sep)
        self.app_layout.insertWidget(true_index, sep)
        self.app_layout.insertWidget(true_index+1, cell_widget)
        return cell_widget

    def add_cell_widget(self, name, collapse):
        cell_widgets = self.get_all_cell_widget()
        cell_widget_names = [widget.name for widget in cell_widgets]
        name = name.upper()
        if name in cell_widget_names:
            return
        cell_widget = app_cell_widget.AppCellWidget(name, collapse, self)
        cell_widget.delete_signal.connect(self.delete_separator)
        sep = Separator()
        sep.widget_name = name
        self.separators.append(sep)
        self.app_layout.addWidget(sep)
        self.app_layout.addWidget(cell_widget)
        return cell_widget

    def init(self):
        app_conf_path = self.get_app_conf_path()
        if not os.path.isfile(app_conf_path):
            return
        cp = conf_parser.ConfParser(app_conf_path)
        conf_data = cp.parse().get()
        sorted_group = sorted(conf_data, key=lambda i: conf_data[i]["order"])
        for group_name in sorted_group:
            collapse = conf_data[group_name]["collapse"]
            cell_widget = self.add_cell_widget(group_name, collapse)
            if not conf_data[group_name]. has_key("apps"):
                continue
            apps_dict = conf_data[group_name]["apps"]
            if not apps_dict:
                continue
            for app_name in apps_dict:
                path = apps_dict[app_name]
                cell_widget.append_app_btn(app_name, path)

    @staticmethod
    def get_app_conf_path():
        app_conf_path = get_conf_path.get_conf_path("app.yml")
        return app_conf_path

    def delete_separator(self, widget_name):
        for sep in self.separators:
            if sep.widget_name == widget_name:
                sep.deleteLater()

    def get_all_cell_widget(self):
        cell_widgets = list()
        app_layout = self.app_layout
        for i in xrange(app_layout.count()):
            item = app_layout.itemAt(i)
            widget = item.widget()
            if not hasattr(widget, "name"):
                continue
            cell_widgets.append(widget)
        return cell_widgets

    def get_all_app(self):
        all_app = list()
        cell_widgets = self.get_all_cell_widget()
        if not cell_widgets:
            return
        for widget in cell_widgets:
            all_app.extend(widget.apps)
        return all_app
