# -*- coding: utf-8 -*-
from __future__ import division
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from .user_display import UserDisplay
from .app_widget import AppWidget
from .recent_app import RecentApp
from ..frameworks.separator import Separator
from ..frameworks.search_line_edit import SearchLineEdit
from ..libs import conf_parser, get_icon_path
from ..libs import get_conf_path, remove_dir, start_file, recent_operation


class PopupDialog(QDialog):
    def __init__(self, parent=None):
        super(PopupDialog, self).__init__(parent)
        self.setWindowTitle("Insert Group")
        self.resize(300, 100)
        self.result = None
        self.setup_ui()
        self.set_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        value_layout = QGridLayout()
        index_label = QLabel("Row")
        self.index_spin = QSpinBox()
        self.index_spin.setRange(1, 500)
        self.index_spin.setValue(1)
        name_label = QLabel("Name")
        self.name_le = QLineEdit()
        value_layout.addWidget(index_label, 0, 0)
        value_layout.addWidget(self.index_spin, 0, 1)
        value_layout.addWidget(name_label, 1, 0)
        value_layout.addWidget(self.name_le, 1, 1)
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(value_layout)
        main_layout.addLayout(btn_layout)

    def set_signals(self):
        self.ok_btn.clicked.connect(self.get_result)
        self.cancel_btn.clicked.connect(self.do_close)

    def get_result(self):
        index = self.index_spin.value()
        name = self.name_le.text()
        self.result = [index, name]
        self.close()
        self.deleteLater()

    def do_close(self):
        self.result = None
        self.close()
        self.deleteLater()


class AppManager(QDialog):
    def __init__(self, parent=None):
        super(AppManager, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("APP Manager")
        icon = get_icon_path.get_icon_path("app.png")
        self.setWindowIcon(QIcon(icon))
        self.setup_ui()
        self.init_size()
        self.init_opacity()
        self.init_search_completer()
        self.set_style()
        self.set_signals()
        self.collapse_status = True

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 10, 0, 0)
        self.user_display_widget = UserDisplay(self)
        main_layout.addWidget(self.user_display_widget)
        sep = Separator()
        main_layout.addWidget(sep)
        # search widget
        self.search_le = SearchLineEdit(self)
        main_layout.addWidget(self.search_le)
        sep1 = Separator()
        main_layout.addWidget(sep1)
        # scroll area
        scroll_area = QScrollArea()
        scroll_area.setObjectName("scroll")
        scroll_area.setStyleSheet("#scroll{border: 0px solid;}")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll_area)
        # scroll widget
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(5, 0, 5, 5)
        scroll_layout.setAlignment(Qt.AlignTop)
        self.recent_app_widget = RecentApp(self)
        self.app_widget = AppWidget(self)
        scroll_layout.addWidget(self.recent_app_widget)
        scroll_layout.addWidget(self.app_widget)
        # slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setPageStep(5)
        self.slider.setValue(100)
        self.slider.setMinimumHeight(12)
        main_layout.addWidget(self.slider)

    def init_size(self):
        size_conf_path = get_conf_path.get_conf_path("size.yml")
        cp = conf_parser.ConfParser(size_conf_path)
        size_conf_data = cp.parse().get()
        if not size_conf_data:
            self.resize(380, 650)
            return
        size = size_conf_data["size"]
        self.resize(*size)

    def init_opacity(self):
        opacity_conf_path = get_conf_path.get_conf_path("opacity.yml")
        cp = conf_parser.ConfParser(opacity_conf_path)
        opacity_conf_data = cp.parse().get()
        if not opacity_conf_data:
            self.setWindowOpacity(1)
            return
        opacity = opacity_conf_data["opacity"]
        self.slider.setValue(opacity*100)
        self.setWindowOpacity(opacity)

    def init_search_completer(self):
        apps = self.app_widget.get_all_app()
        if not apps:
            return
        app_names = [app.name for app in apps]
        self.search_le.set_completer(app_names)

    def set_style(self):
        self.setStyle(QStyleFactory.create('plastique'))
        qss_path = os.path.abspath(os.path.join(__file__, "..", "style.qss"))
        self.setStyleSheet(open(qss_path, 'r').read())

    def set_signals(self):
        self.user_display_widget.add_tool_action.triggered.connect(self.add_tool_group)
        self.user_display_widget.insert_tool_action.triggered.connect(self.insert_tool_group)
        self.user_display_widget.reset_action.triggered.connect(self.reset)
        self.user_display_widget.collapse_all_action.triggered.connect(self.collapse_all)
        self.search_le.returnPressed.connect(self.run_app)
        self.slider.valueChanged.connect(self.set_opacity)

    def run_app(self):
        apps = self.app_widget.get_all_app()
        for app in apps:
            if app.name == self.search_le.text():
                start_file.start_file(app.exe_path)
                recent_operation.save_to_recent(app.name, app.exe_path)
                break

    def add_tool_group(self):
        name, ok = QInputDialog.getText(self, "Group Name", "Please input a group name")
        if not ok:
            return
        if name and ok:
            self.app_widget.add_cell_widget(name, False)

    def insert_tool_group(self):
        popup_dialog = PopupDialog(self)
        popup_dialog.exec_()
        result = popup_dialog.result
        if result is None:
            return
        else:
            index, name = result
            self.app_widget.insert_cell_widget(name, False, index)

    def reset(self):
        msg_box = QMessageBox.information(self, "Warming Tip", "Do you really want to reset?",
                                                QMessageBox.Yes | QMessageBox.No)
        if msg_box.name == "No":
            return
        self.close()
        conf_dir = get_conf_path.get_app_conf_dir()
        remove_dir.remove_dir(conf_dir)
        self.deleteLater()

    def closeEvent(self, event):
        self.save_modified_settings()
        self.save_size()
        self.save_opacity()

    def collapse_all(self):
        cell_widgets = self.app_widget.get_all_cell_widget()
        for widget in cell_widgets:
            if self.collapse_status:
                widget.main_layout.set_collapse()
            else:
                widget.main_layout.set_expand()
        self.collapse_status = not self.collapse_status

    def save_modified_settings(self):
        cell_widgets = self.app_widget.get_all_cell_widget()
        if not cell_widgets:
            return
        app_conf_data = dict()
        app_conf_path = self.app_widget.get_app_conf_path()
        for index, widget in enumerate(cell_widgets):
            group_name = str(widget.name)
            order = index
            collapse = widget.layout().collapse_status
            apps = widget.apps
            app_dict = dict()
            if apps:
                for app in apps:
                    app_dict[app.name] = app.exe_path
            app_conf_data[group_name] = dict(order=order, collapse=collapse, apps=app_dict)
        cp = conf_parser.ConfParser(app_conf_path)
        cp.parse().set(app_conf_data)

    def save_size(self):
        size_conf_path = get_conf_path.get_conf_path("size.yml")
        cp = conf_parser.ConfParser(size_conf_path)
        width = self.width()
        height = self.height()
        new_data = {"size": [width, height]}
        cp.parse().set(new_data)

    def save_opacity(self):
        size_conf_path = get_conf_path.get_conf_path("opacity.yml")
        cp = conf_parser.ConfParser(size_conf_path)
        opacity = self.windowOpacity()
        new_data = {"opacity": opacity}
        cp.parse().set(new_data)

    def move_to_corner(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())-15, (screen.height()-size.height()-80))

    def set_opacity(self, value):
        self.setWindowOpacity(value/100)
