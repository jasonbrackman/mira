# -*- coding: utf-8 -*-
import os
from PySide import QtGui, QtCore
from miraLibs.pipeLibs.pipeDb import get_members
from miraLibs.pyLibs import yml_operation, join_path
from miraLibs.pipeLibs.pipeDb import sql_api

QSS_PATH = join_path.join_path2(os.path.dirname(__file__), "style.qss")


class QcerListWidget(QtGui.QListWidget):
    drop = QtCore.Signal()

    def __init__(self, parent=None):
        super(QcerListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.remove_action = QtGui.QAction("remove", self)
        self.remove_action.triggered.connect(self.remove_selected_item)
        self.drop.connect(self.drop_in)

    def show_context_menu(self, pos):
        global_pos = self.mapToGlobal(pos)
        menu = QtGui.QMenu()
        menu.addAction(self.remove_action)
        menu.exec_(global_pos)

    def dropEvent(self, event):
        super(QcerListWidget, self).dropEvent(event)
        self.drop.emit()

    def add_items(self, text_list):
        if not text_list:
            return
        for text in text_list:
            item = QtGui.QListWidgetItem(text)
            self.addItem(item)

    def remove_selected_item(self):
        selected_items = self.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.takeItem(self.row(item))

    def get_items_text(self):
        items_text = list()
        row_count = self.count()
        if row_count:
            for row in xrange(row_count):
                item = self.item(row)
                items_text.append(item.text())
        return items_text

    def drop_in(self):
        items_text = list(set(self.get_items_text()))
        self.clear()
        self.add_items(items_text)


class QcerConfig(QtGui.QMainWindow):
    def __init__(self, project=None, parent=None):
        super(QcerConfig, self).__init__(parent)
        self.resize(550, 500)
        self.setWindowTitle("Qcer Configuration")
        self.project = project
        self.db = sql_api.SqlApi(self.project)
        self.setup_ui()
        self.init()
        self.set_signals()
        self.set_style()

    def setup_ui(self):
        central_widget = QtGui.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtGui.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        user_layout = QtGui.QHBoxLayout()
        self.group_list = QtGui.QListWidget()
        self.group_member_list = QtGui.QListWidget()
        self.group_member_list.setDragEnabled(True)
        self.group_member_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        space_label = QtGui.QLabel("===>")

        config_layout = QtGui.QVBoxLayout()
        self.context_combo = QtGui.QComboBox()
        table_group = QtGui.QGroupBox()
        group_layout = QtGui.QVBoxLayout(table_group)
        group_layout.setContentsMargins(0, 0, 0, 0)
        self.qcer_table = QtGui.QTableWidget()
        group_layout.addWidget(self.qcer_table)
        self.qcer_table.setColumnCount(2)
        self.qcer_table.horizontalHeader().setDefaultSectionSize(50)
        self.qcer_table.horizontalHeader().setClickable(False)
        self.qcer_table.horizontalHeader().setStretchLastSection(True)
        self.qcer_table.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.qcer_table.setHorizontalHeaderLabels(["step", "QCer"])
        self.qcer_table.verticalHeader().setVisible(False)
        self.qcer_table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.qcer_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        config_layout.addWidget(self.context_combo)

        config_btn_layout = QtGui.QHBoxLayout()
        self.add_btn = QtGui.QToolButton()
        self.add_btn.setText("+")
        self.remove_btn = QtGui.QToolButton()
        self.remove_btn.setText("-")
        self.save_btn = QtGui.QPushButton("Save")
        config_btn_layout.addStretch()
        config_btn_layout.addWidget(self.add_btn)
        config_btn_layout.addWidget(self.remove_btn)
        config_btn_layout.addWidget(self.save_btn)
        group_layout.addLayout(config_btn_layout)

        config_layout.addWidget(table_group)

        user_layout.addWidget(self.group_list)
        user_layout.addWidget(self.group_member_list)
        user_layout.addWidget(space_label)
        user_layout.addLayout(config_layout)
        user_layout.setStretch(0, 1)
        user_layout.setStretch(1, 1.8)
        user_layout.setStretch(2, 0.5)
        user_layout.setStretch(3, 3)

        buttom_layout = QtGui.QHBoxLayout()
        self.config_btn = QtGui.QPushButton("Config")
        buttom_layout.addWidget(self.config_btn)

        main_layout.addLayout(user_layout)
        main_layout.addLayout(buttom_layout)

    def set_style(self):
        self.setStyle(QtGui.QStyleFactory.create('plastique'))
        self.setStyleSheet(open(QSS_PATH, 'r').read())

    @staticmethod
    def get_member_dict():
        all_staff_dict = get_members.JRF_staff_DB('JRF_baseInfo', 'staff').getAll()
        res_dict = {}
        for key in all_staff_dict.keys():
            department = all_staff_dict[key]['department']
            name = all_staff_dict[key]["name"]
            if not res_dict.__contains__(department):
                res_dict[department] = []
            res_dict[department].append(key+'_'+name)
        return res_dict

    def init(self):
        self.init_group_list()
        self.init_context_combo()

    def init_group_list(self):
        res_dict = self.get_member_dict()
        for group in res_dict:
            item = QtGui.QListWidgetItem(group)
            item.group_members = res_dict[group]
            self.group_list.addItem(item)

    def get_context_qcer(self, context):
        context_qcer_data = self.db.getQCConfig()
        if context_qcer_data:
            context_qcer_data = eval(context_qcer_data)
            if context in context_qcer_data:
                return context_qcer_data[context]

    def init_context_combo(self):
        conf_path = os.path.join(os.path.dirname(__file__), "context.yml")
        context_data = yml_operation.get_yaml_data(conf_path)
        contexts = context_data["contexts"].split(",")
        self.context_model = QtGui.QStandardItemModel()
        for context in contexts:
            item = QtGui.QStandardItem(context)
            item.qcer = self.get_context_qcer(context)
            self.context_model.appendRow(item)
        self.context_combo.setModel(self.context_model)
        self.context_combo.setCurrentIndex(self.context_combo.count()+1)

    def set_signals(self):
        self.group_list.itemClicked.connect(self.show_group_members)
        self.context_combo.currentIndexChanged[int].connect(self.show_qcer)
        self.config_btn.clicked.connect(self.do_config)
        self.add_btn.clicked.connect(self.add_step)
        self.remove_btn.clicked.connect(self.remove_selected_rows)
        self.save_btn.clicked.connect(self.set_context_qcer)

    def show_group_members(self, item):
        self.group_member_list.clear()
        self.group_member_list.addItems(item.group_members)

    def add_table_row(self, row, step='', step_qcer=[]):
        step_item = QtGui.QTableWidgetItem(step)
        self.qcer_table.setItem(row, 0, step_item)
        qcer_widget = QcerListWidget()
        qcer_widget.add_items(step_qcer)
        self.qcer_table.setCellWidget(row, 1, qcer_widget)
        self.qcer_table.setRowHeight(row, 100)

    def add_step(self):
        row_count = self.qcer_table.rowCount()
        self.qcer_table.setRowCount(row_count+1)
        self.add_table_row(row_count)

    def remove_table_all(self):
        for row in xrange(self.qcer_table.rowCount()):
            self.qcer_table.removeRow(0)

    def remove_selected_rows(self):
        selected_indexes = self.qcer_table.selectedIndexes()
        rows = list(set([index.row() for index in selected_indexes]))
        for row in rows:
            self.qcer_table.removeRow(row)

    def show_qcer(self, context_index):
        self.remove_table_all()
        current_item = self.context_model.item(context_index)
        qcer_dict = current_item.qcer
        if not qcer_dict:
            return
        steps = sorted(qcer_dict, key=lambda key: qcer_dict[key]["order"])
        self.qcer_table.setRowCount(len(steps))
        for index, step in enumerate(steps):
            step_qcer = current_item.qcer[step]["qcer"]
            self.add_table_row(index, step, step_qcer)

    def get_current_combo_item(self):
        current_index = self.context_combo.currentIndex()
        item = self.context_model.item(current_index)
        return item

    def set_context_qcer(self):
        current_context_item = self.get_current_combo_item()
        current_context_item.qcer = dict()
        for row in xrange(self.qcer_table.rowCount()):
            step = self.qcer_table.item(row, 0).text()
            step_qcer = self.qcer_table.cellWidget(row, 1).get_items_text()
            current_context_item.qcer[step] = {"order": row, "qcer": step_qcer}

    def do_config(self):
        try:
            final_config_data = dict()
            for row in xrange(self.context_model.rowCount()):
                item = self.context_model.item(row)
                context = str(item.text())
                final_config_data[context] = item.qcer
            self.db.addQCConfig(str(final_config_data).replace("'", '"'))
            QtGui.QMessageBox.information(self, "warming tip", "Config done.")
        except Exception as e:
            QtGui.QMessageBox.critical(self, "Error", "Config fail: %s" % str(e))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    qc = QcerConfig("sct")
    qc.show()
    app.exec_()
