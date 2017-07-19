# -*- coding: utf-8 -*-
import getpass
import os
from functools import partial

from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *

import run_send_command
from CommandOperation import CommandOperation
from configure_command import ConfigureCommand
from miraFramework.Filter import Filter
from miraLibs.osLibs import get_local_ip
from miraLibs.pyLibs import ConfParser
from miraLibs.pyLibs.socketLibs import ping_quick
from miraLibs.redisLibs import user_settings, connect_redis, ping_redis

REDIS_HOST = "192.168.0.133"
REDIS_PORT = 6379
CONNECTION_PORT = ConfParser.ConfParser(__file__).conf_data.get("port")
ICON_DIR = os.path.abspath(os.path.join(__file__, "..", "icons"))
GREEN_ICON = os.path.join(ICON_DIR, "green_bullet.png").replace("\\", "/")
RED_ICON = os.path.join(ICON_DIR, "red_bullet.png").replace("\\", "/")
UPDATE_ICON = os.path.join(ICON_DIR, "update.png").replace("\\", "/")


class RedisDialog(QDialog):
    def __init__(self, parent=None):
        super(RedisDialog, self).__init__(parent)
        self.result = None
        self.resize(250, 100)
        self.setWindowTitle("Redis settings")
        main_layout = QGridLayout(self)
        server_label = QLabel("Server")
        port_label = QLabel("Port")
        self.server_le = QLineEdit()
        self.server_le.setText(REDIS_HOST)
        self.port_le = QLineEdit()
        self.port_le.setText(str(REDIS_PORT))
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")
        main_layout.addWidget(server_label, 0, 0, 1, 1)
        main_layout.addWidget(self.server_le, 0, 1, 1, 4)
        main_layout.addWidget(port_label, 1, 0, 1, 1)
        main_layout.addWidget(self.port_le, 1, 1, 1, 4)
        main_layout.addWidget(self.ok_btn, 2, 3, 1, 1)
        main_layout.addWidget(self.cancel_btn, 2, 4, 1, 1)

        self.ok_btn.clicked.connect(self.set_result)
        self.cancel_btn.clicked.connect(self.close)

    def set_result(self):
        server = str(self.server_le.text())
        port = int(self.port_le.text())
        if all((server, port)):
            self.result = dict(server=server, port=port)
        self.close()


class UserItem(object):
    def __init__(self, status="", name=None, host=None, port=None, mac=None):
        self.status = status
        self.name = name
        self.host = host
        self.port = port
        self.mac = mac


class UserDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(UserDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if not index.isValid:
            return
        if index.column() == 0:
            editor = QLabel(parent)
            editor.index = index
            return editor

    def setEditorData(self, editor, index):
        if not index.isValid:
            return
        user_item_proxy_index = index.model().index(index.row(), 4)
        user_item_index = index.model().mapToSource(user_item_proxy_index)
        user_item = user_item_index.data()
        if index.column() == 0:
            status = ping_quick.ping_quick(user_item.host, user_item.port, 0.1)
            user_item.status = status
            if status:
                pix_map_path = GREEN_ICON
            else:
                pix_map_path = RED_ICON
            pixmap = QPixmap(pix_map_path)
            editor.setPixmap(pixmap)

    def updateEditorGeometry(self, editor, option, index):
        if not index.isValid:
            return
        editor.setGeometry(option.rect)


class UserModel(QAbstractTableModel):
    def __init__(self, arg=[], parent=None):
        super(UserModel, self).__init__(parent)
        self.arg = arg
        self.header = ["status", "name", "ip", "mac", ""]

    def rowCount(self, parent=QModelIndex()):
        return len(self.arg)

    def columnCount(self, parent=QModelIndex()):
        return 5

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.arg[row][column]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role=Qt.DisplayRole):
        if not index.isValid():
            return
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.arg[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]


class SendCommandUI(QMainWindow):
    def __init__(self, parent=None):
        super(SendCommandUI, self).__init__(parent)
        self.setWindowTitle("Send Command")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.resize(700, 500)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(2, 3, 2, 3)
        main_layout.addLayout(self.create_status_layout())
        main_layout.addWidget(self.create_user_info_group())
        main_layout.addLayout(self.create_command_layout())
        main_layout.addLayout(self.create_button_layout())
        self.create_action()
        self.create_menu()
        self.set_signals()

        self.redis_host = REDIS_HOST
        self.redis_port = REDIS_PORT
        self.connection_port = CONNECTION_PORT
        self.command_operation = CommandOperation()
        self.refresh()

    def create_status_layout(self):
        status_layout = QHBoxLayout()
        status_label = QLabel()
        status_label.setText("<font color=#FF9c20>Redis connection status:</font>")
        self.status_view = QLabel()
        self.refresh_btn = QToolButton()
        self.refresh_btn.setIcon(QIcon(UPDATE_ICON))
        self.refresh_btn.setStyleSheet("background: transparent;")
        status_layout.addStretch()
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_view)
        status_layout.addWidget(self.refresh_btn)
        return status_layout

    def create_user_info_group(self):
        user_info_grp = QGroupBox("User Info")
        user_info_layout = QVBoxLayout(user_info_grp)
        filter_layout = QHBoxLayout()
        self.filter_le = Filter()
        self.user_count_label = QLabel()
        filter_layout.addWidget(self.user_count_label)
        filter_layout.addStretch()
        filter_layout.addWidget(self.filter_le)
        self.user_info_view = QTableView()
        self.user_info_view.verticalHeader().hide()
        self.user_info_view.setAlternatingRowColors(True)
        self.user_info_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.user_info_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        user_info_layout.addLayout(filter_layout)
        user_info_layout.addWidget(self.user_info_view)
        return user_info_grp

    def create_command_layout(self):
        command_layout = QHBoxLayout()
        command_label = QLabel("Command")
        self.command_combo = QComboBox()
        command_layout.addWidget(command_label)
        command_layout.addWidget(self.command_combo)
        command_layout.setStretchFactor(command_label, 1)
        command_layout.setStretchFactor(self.command_combo, 15)
        return command_layout

    def create_button_layout(self):
        btn_layout = QHBoxLayout()
        self.test_btn = QPushButton("Local Test")
        self.send_selected_btn = QPushButton("Send To Selected")
        self.send_all_btn = QPushButton("Send To All")
        btn_layout.addStretch()
        btn_layout.addWidget(self.test_btn)
        btn_layout.addWidget(self.send_selected_btn)
        btn_layout.addWidget(self.send_all_btn)
        return btn_layout

    def create_action(self):
        self.set_redis_action = QAction("Redis Server", self)
        self.set_port_action = QAction("Connection Port", self)
        self.configure_command_action = QAction("Configure Command", self)

    def create_menu(self):
        self.file_menu = QMenu("File", self)
        self.file_menu.addAction(self.set_redis_action)
        self.file_menu.addAction(self.set_port_action)
        self.file_menu.addAction(self.configure_command_action)
        self.menuBar().addMenu(self.file_menu)

    def set_signals(self):
        self.send_selected_btn.clicked.connect(partial(self.send_command, False))
        self.send_all_btn.clicked.connect(partial(self.send_command, True))
        self.test_btn.clicked.connect(self.local_test)
        self.set_redis_action.triggered.connect(self.set_redis)
        self.set_port_action.triggered.connect(self.set_port)
        self.configure_command_action.triggered.connect(self.configure_command)
        self.refresh_btn.clicked.connect(self.refresh)

    def set_redis(self):
        rd = RedisDialog(self)
        rd.exec_()
        result_data = rd.result
        if not result_data:
            return
        self.redis_host = result_data["server"]
        self.redis_port = result_data["port"]
        self.refresh()

    def set_port(self):
        input_port = QInputDialog.getInteger(self, "Connection Port", "Please Input Port", self.connection_port)
        if input_port[1]:
            self.connection_port = input_port[0]

    def configure_command(self):
        cc = ConfigureCommand(self)
        cc.exec_()
        result = cc.result
        if not result:
            return
        self.command_operation.set_command(**result)
        self.command_combo.clear()
        self.init_commands()

    def init(self):
        self.conn = connect_redis.connect_redis(self.redis_host, self.redis_port)
        self.conn_status = ping_redis.ping_redis(self.conn)
        if self.conn_status:
            pix_map = QPixmap(GREEN_ICON)
        else:
            pix_map = QPixmap(RED_ICON)
        self.status_view.setPixmap(pix_map)

    def init_commands(self):
        self.command_dict = self.command_operation.get_command()
        for key in self.command_dict:
            self.command_combo.addItem(key)
        self.command_combo.setCurrentIndex(self.command_combo.count()+1)

    def get_model_data(self):
        model_data = list()
        user_info = user_settings.get_user_info(self.conn, ["name", "ip", "mac"])
        if user_info:
            for user in user_info:
                name = user["name"]
                host = user["ip"]
                mac = user["mac"]
                port = self.connection_port
                user_item = UserItem("", name, host, port, mac)
                model_data.append(["", name, host, mac, user_item])
        else:
            model_data = [[]]
        return model_data

    def set_model(self):
        if not self.conn_status:
            model_data = [[]]
        else:
            model_data = self.get_model_data()
        user_count = len(model_data)
        self.user_count_label.setText("User Count: <font size=5 color=#0000FF><b>%s</b></font>" % user_count)
        if model_data == [[]]:
            model = QStandardItemModel()
            self.user_info_view.setModel(model)
            return
        self.model = UserModel(model_data, self.user_info_view)
        self.proxy_model = QSortFilterProxyModel()
        self.filter_le.textChanged.connect(self.set_filter)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(-1)
        self.user_info_view.setModel(self.proxy_model)
        self.user_info_view.setSortingEnabled(True)
        self.user_info_view.hideColumn(4)
        self.user_info_view.horizontalHeader().setStretchLastSection(True)
        column_width_list = [20, 200, 200, 200]
        for column in range(4):
            self.user_info_view.setColumnWidth(column, column_width_list[column])

    def set_delegate(self):
        image_delegate = UserDelegate(self.user_info_view)
        self.user_info_view.setItemDelegate(image_delegate)

    def show_delegate(self):
        for i in xrange(self.proxy_model.rowCount()):
            self.user_info_view.openPersistentEditor(self.proxy_model.index(i, 0))
            self.user_info_view.openPersistentEditor(self.proxy_model.index(i, 3))

    def refresh(self):
        self.init()
        self.init_commands()
        self.set_model()
        self.set_delegate()
        self.show_delegate()

    def set_filter(self, text):
        self.proxy_model.setFilterRegExp(text)
        self.show_delegate()

    def get_selection_items(self, whole=False):
        items = list()
        if whole:
            rows = xrange(self.model.rowCount())
        else:
            proxy_indexes = self.user_info_view.selectedIndexes()
            rows = list(set([self.proxy_model.mapToSource(i).row() for i in proxy_indexes]))
        if rows:
            items = [self.model.index(row, 4).data() for row in rows]
        return items

    def send_command(self, whole):
        command_title = self.command_combo.currentText()
        command = self.command_dict[command_title]
        if not command:
            return
        items = self.get_selection_items(whole)
        if not items:
            return
        for item in items:
            if item.status:
                user = dict(name=item.name, ip=item.host)
                run_send_command.send_user_command(user, self.connection_port, command)

    def local_test(self):
        command_title = self.command_combo.currentText()
        command = self.command_dict[command_title]
        if not command:
            return
        local_user = getpass.getuser()
        local_ip = get_local_ip.get_local_ip()
        user = dict(name=local_user, ip=local_ip)
        if ping_quick.ping_quick(local_ip, self.connection_port, 0.1):
            run_send_command.send_user_command(user, self.connection_port, command)
        else:
            QMessageBox.critical(None, "warming Tip",
                                       "Can't make connection %s %s" % (local_ip, self.connection_port))


def main():
    import sys
    app = QApplication(sys.argv)
    sc = SendCommandUI()
    sc.show()
    app.exec_()


if __name__ == "__main__":
    main()
