# -*- coding: utf-8 -*-
import os
import logging
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from libs import get_context, get_context_conf_path, add_environ, \
    get_check_py_file, conf_parser, select_node, get_parent_win, get_icon_path


logger = logging.getLogger("PREFLIGHT")


class ScriptError(RuntimeError):
    pass


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.set_status("default")

    def set_status(self, status):
        icon_path = get_icon_path.get_icon_path(status)
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(20, 20)
        self.setPixmap(pixmap)


class CheckButton(QPushButton):
    def __init__(self, name, module_name, description, ignorable, parent=None):
        super(CheckButton, self).__init__(parent)
        self.setMinimumWidth(200)
        self.name = name
        self.module_name = module_name
        self.description = description
        self.ignorable = ignorable
        self.setText(self.name)
        self.menu = QMenu(self)
        self.description_action = QAction("Description...", self)

    def contextMenuEvent(self, event):
        self.menu.clear()
        self.menu.addAction(self.description_action)
        self.menu.exec_(QCursor.pos())
        event.accept()


class FailDialog(QDialog):
    def __init__(self, module_name, ignorable, can_auto, check_object, label, parent=None):
        super(FailDialog, self).__init__(parent)
        self.has_error = False
        self.close_error = True
        self.resize(400, 400)
        self.flags = self.windowFlags()
        self.module_name = module_name
        self.setWindowTitle(self.module_name)
        self.ignorable = ignorable
        self.can_auto = can_auto
        self.check_object = check_object
        self.label = label
        self.setup_ui()
        self.init()
        self.set_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        check_file_label = QLabel("<font size=>Check file</font>")
        self.check_file_le = QLineEdit()
        self.check_file_le.setReadOnly(True)
        error_info_label = QLabel("<font size=4>Error information</font>")
        self.error_info_text = QTextEdit()
        self.error_info_text.setFont(QFont("Courier", 10))
        self.error_info_text.setMaximumHeight(80)
        self.error_info_text.setReadOnly(True)
        error_list_label = QLabel("<font size=4>Error list</font>")
        self.error_list_widget = QListWidget()
        self.error_list_widget.setSortingEnabled(True)
        self.error_list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        btn_layout = QHBoxLayout()
        self.ignore_btn = QPushButton(u"Ignore忽略 I")
        self.ignore_btn.setShortcut("I")
        self.auto_btn = QPushButton(u"Auto自动 A")
        self.auto_btn.setShortcut("A")
        self.manual_btn = QPushButton(u"manual手动 M")
        self.manual_btn.setShortcut("M")
        btn_layout.addWidget(self.ignore_btn)
        btn_layout.addWidget(self.auto_btn)
        btn_layout.addWidget(self.manual_btn)
        main_layout.addWidget(check_file_label)
        main_layout.addWidget(self.check_file_le)
        main_layout.addWidget(error_info_label)
        main_layout.addWidget(self.error_info_text)
        main_layout.addWidget(error_list_label)
        main_layout.addWidget(self.error_list_widget)
        main_layout.addLayout(btn_layout)

    def init(self):
        py_file = get_check_py_file.get_check_py_file(self.module_name)
        error_list = self.check_object.error_list
        self.check_file_le.setText(py_file)
        if py_file and os.path.isfile(py_file):
            self.check_file_le.setStyleSheet("")
        else:
            self.check_file_le.setStyleSheet("color: #FF0000")
        if not self.ignorable:
            self.ignore_btn.setEnabled(False)
        if not self.can_auto:
            self.auto_btn.setEnabled(False)
        self.error_info_text.setText(self.check_object.info)
        if error_list:
            self.error_list_widget.addItems(error_list)

    def set_signals(self):
        self.ignore_btn.clicked.connect(self.do_ignore)
        self.auto_btn.clicked.connect(self.do_auto)
        self.manual_btn.clicked.connect(self.do_manual)
        self.error_list_widget.itemSelectionChanged.connect(self.select_maya)
        self.error_list_widget.itemClicked.connect(self.do_item_clicked)

    def do_ignore(self):
        self.label.set_status("ignore")
        self.has_error = False
        self.close_error = False
        self.close()

    def do_auto(self):
        try:
            self.check_object.auto_solve()
            self.error_list_widget.clear()
            if self.check_object.error_list:
                self.error_list_widget.addItems(self.check_object.error_list)
        except Exception as e:
            logger.error(str(e))
            QMessageBox.critical(self, "Warming Tip", u"Script Error, Connect TD.脚本错误，联系TD")
            self.auto_btn.setStyleSheet("background: #FF0000")
            self.do_manual()
        else:
            self.label.set_status(self.check_object.check_result)
            if self.check_object.check_result == "fail":
                self.auto_btn.setStyleSheet("background: #FF0000")
                self.do_manual()
            elif self.check_object.check_result == "pass":
                logger.info(self.check_object.info)
                self.close_error = False
                self.close()
            elif self.check_object.check_result == "warning":
                logger.warning(self.check_object.info)
                self.close_error = False
                self.close()

    def select_clicked(self, item):
        node = item.text()
        select_node.select_node(node)

    def do_manual(self):
        self.setModal(False)
        self.check_object.close()
        if not self.error_list_widget.count():
            self.close()
        self.has_error = True

    def do_item_clicked(self, item):
        self.select_clicked(item)
        self.do_manual()

    def select_maya(self):
        selected_items = self.error_list_widget.selectedItems()
        if not selected_items:
            return
        nodes = [item.text() for item in selected_items]
        select_node.select_node(nodes)

    def closeEvent(self, event):
        self.has_error = self.close_error


class CheckGui(QDialog):
    def __init__(self, parent=None):
        super(CheckGui, self).__init__(parent)
        add_environ.add_environ()
        self.setObjectName("PREFLIGHT")
        self.context = get_context.get_context()
        self.setWindowTitle("%s preflight" % self.context)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.resize(420, 600)
        self.setup_ui()
        self.set_signals()
        self.init_table_widget()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("<font size=4><b>Current Step:</b></font>"
                                  "<font size=5 color=#ff8c00><b> %s</b></font>" % self.context)
        main_layout.addWidget(self.label)
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setAutoFillBackground(True)
        main_layout.addWidget(main_splitter)

        self.table_widget = QTableWidget()
        self.table_widget.setFocusPolicy(Qt.NoFocus)
        main_splitter.insertWidget(0, self.table_widget)

        bottom_widget = QWidget()
        main_splitter.insertWidget(1, bottom_widget)
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        btn_layout = QHBoxLayout()
        self.check_all_btn = QPushButton("Check All")
        btn_layout.addStretch()
        btn_layout.addWidget(self.check_all_btn)
        self.text_browser = QTextBrowser()
        self.text_browser.setReadOnly(True)
        self.text_browser.setFont(QFont("Courier", 10))

        bottom_layout.addLayout(btn_layout)
        bottom_layout.addWidget(self.text_browser)
        main_splitter.setSizes([545, 55])
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 0)

    def set_signals(self):
        self.check_all_btn.clicked.connect(self.do_check_all)

    def init_table_widget(self):
        self.table_widget .horizontalHeader().setStretchLastSection(True)
        self.table_widget.setColumnCount(3)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        header_list = ["mandatory", "check options", "result"]
        self.table_widget.setHorizontalHeaderLabels(header_list)
        self.set_header_style()
        self.set_cell_widget()
        self.table_widget.resizeColumnToContents(0)
        self.table_widget.resizeColumnToContents(1)
        self.table_widget.resizeColumnToContents(2)
        self.table_widget.setColumnWidth(2, 30)

    def set_header_style(self):
        font_size = 10
        horizontal_header = self.table_widget.horizontalHeader()
        # horizontal_header.setClickable(False)
        font = QFont()
        font.setPointSizeF(font_size)
        font.setWeight(QFont.Bold)
        horizontal_header.setFont(font)
        horizontal_header.setStyleSheet("QHeaderView{color: #DDDDDD}")

    def set_cell_widget(self):
        conf_path = get_context_conf_path.get_context_conf_path()
        if (not conf_path) or (not os.path.isfile(conf_path)):
            QMessageBox.critical(self, "Critical", "This context has no configuration .yml file.")
            return
        cp = conf_parser.ConfParser(conf_path)
        conf_data = cp.parse().get()
        check_options = sorted(conf_data, key=lambda key: conf_data[key]["order"])
        self.table_widget.setRowCount(len(check_options))
        for index, check_option in enumerate(check_options):
            # set column 1/ checkbox
            check_cbox = QCheckBox()
            check_cbox.setChecked(True)
            check_cbox.index = (index, 0)
            check_cbox.stateChanged.connect(self.set_option_checked)
            self.table_widget.setCellWidget(index, 0, check_cbox)
            # set column 2/ pushbutton
            name = conf_data[check_option]["name"]
            description = conf_data[check_option]["description"]
            ignorable = conf_data[check_option]["ignorable"]
            check_btn = CheckButton(name, check_option, description, ignorable, self)
            check_btn.description_action.triggered.connect(self.show_description)
            check_btn.clicked.connect(self.check_option)
            check_btn.index = (index, 1)
            self.table_widget.setCellWidget(index, 1, check_btn)
            # set column 3/ label
            label = ImageLabel(self)
            label.setMinimumWidth(100)
            label.index = (index, 2)
            self.table_widget.setCellWidget(index, 2, label)

    def show_description_information(self, widget):
        description_info = widget.description
        check_file = get_check_py_file.get_check_py_file(widget.module_name)
        show_info = "%s\n\ncheck file:\n%s" % (description_info, check_file)
        self.text_browser.setText(show_info)
        if check_file and os.path.isfile(check_file):
            self.text_browser.setStyleSheet("")
        else:
            self.text_browser.setStyleSheet("color: #FF0000")

    def show_description(self):
        self.show_description_information(self.sender().parent())

    def set_option_checked(self):
        index = self.sender().index
        check_btn = self.table_widget.cellWidget(index[0], 1)
        if not self.sender().isChecked():
            check_btn.setEnabled(False)
        else:
            check_btn.setEnabled(True)

    def check_option(self):
        self.check_single_option(self.sender())

    def check_single_option(self, check_btn):
        if not check_btn.isEnabled():
            return
        self.show_description_information(check_btn)
        index = check_btn.index
        label = self.table_widget.cellWidget(index[0], 2)
        module_name = check_btn.module_name
        ignorable = check_btn.ignorable
        exec("import {0};reload ({0})".format(module_name))
        check_object = eval("{0}.{0}()".format(module_name))
        check_object.set_window_title(check_btn.name)
        check_object.show()
        try:
            check_object.run()
        except Exception as e:
            label.set_status("fail")
            QMessageBox.critical(self, "Warming Tip", u"Script Error,Please connect TD.脚本错误，联系TD.")
            raise ScriptError(str(e))
        else:
            can_auto = True if hasattr(check_object, "auto_solve") else False
            label.set_status(check_object.check_result)
            if check_object.check_result == "pass":
                logger.info(check_object.info)
            elif check_object.check_result == "fail":
                logger.error(check_object.info)
                self.deal_fail(check_btn.module_name, ignorable, can_auto, check_object, label)
            elif check_object.check_result == "warning":
                logger.warning(check_object.info)
        finally:
            check_object.close()

    def deal_fail(self, module_name, ignorable, can_auto, check_object, label):
        self.fd = FailDialog(module_name, ignorable, can_auto, check_object, label, get_parent_win.get_parent_win())
        self.fd.exec_()
        if self.fd.has_error:
            raise RuntimeError("Stop here.")

    def do_check_all(self):
        for i in xrange(self.table_widget.rowCount()):
            label = self.table_widget.cellWidget(i, 2)
            label.set_status("default")
        try:
            for i in xrange(self.table_widget.rowCount()):
                check_btn = self.table_widget.cellWidget(i, 1)
                self.check_single_option(check_btn)
            print "All checks passed"
            return True
        except:
            print "failed"
            return False


def main():
    # global cg
    # try:
    #     cg.close()
    #     cg.deleteLater()
    # except:pass
    # cg = CheckGui(get_parent_win.get_parent_win())
    # cg.show()
    # return cg
    from miraLibs.qtLibs import render_ui
    render_ui.render(CheckGui)


def main_for_publish():
    cg = main()
    result = cg.do_check_all()
    return result, cg
