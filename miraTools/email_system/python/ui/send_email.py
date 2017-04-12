# -*- coding: utf-8 -*-
import socket
import getpass
from PySide import QtGui, QtCore
from ..frameworks import text_edit
from ..frameworks import filter_line_edit, email_button
from .address_book_ui import address_book_tree_ui
from ..libs import redis_api
from ..libs import get_redis_conn
from ..libs import get_current_date


class SendEmailUI(QtGui.QWidget):

    def __init__(self, parent=None):
        super(SendEmailUI, self).__init__(parent)
        main_layout = QtGui.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_group = QtGui.QGroupBox()
        main_layout.addWidget(main_group)
        group_layout = QtGui.QHBoxLayout(main_group)
        group_layout.setContentsMargins(5, 10, 5, 5)
        main_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        group_layout.addWidget(main_splitter)
        left_widget = QtGui.QWidget()
        main_splitter.addWidget(left_widget)
        left_layout = QtGui.QGridLayout(left_widget)
        left_layout.setVerticalSpacing(20)
        acceptor_label = QtGui.QLabel(u"收件人")
        acceptor_label.setAlignment(QtCore.Qt.AlignRight)
        self.acceptor_le = QtGui.QLineEdit()
        title_label = QtGui.QLabel(u"主题")
        title_label.setAlignment(QtCore.Qt.AlignRight)
        self.title_le = QtGui.QLineEdit()
        content_label = QtGui.QLabel(u"正文")
        content_label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        self.content_te = text_edit.TextEdit()
        left_layout.addWidget(acceptor_label, 0, 0, 1, 1)
        left_layout.addWidget(self.acceptor_le, 0, 1, 1, 20)
        left_layout.addWidget(title_label, 1, 0, 1, 1)
        left_layout.addWidget(self.title_le, 1, 1, 1, 20)
        left_layout.addWidget(content_label, 2, 0, 1, 1)
        left_layout.addWidget(self.content_te, 2, 1, 1, 20)

        btn_layout = QtGui.QHBoxLayout()
        self.send_btn = email_button.EmailButton("write", u"发送")
        btn_layout.addStretch()
        btn_layout.addWidget(self.send_btn)
        left_layout.addLayout(btn_layout, 3, 0, 1, 21)

        # address layout
        tab_widget = QtGui.QTabWidget()
        address_widget = QtGui.QWidget()
        address_layout = QtGui.QVBoxLayout(address_widget)
        self.filter_le = filter_line_edit.FilterLineEdit()
        self.address_tree = address_book_tree_ui.AddressBookTreeView()
        address_layout.addWidget(self.filter_le)
        address_layout.addWidget(self.address_tree)
        tab_widget.insertTab(0, address_widget, u"通讯录")
        main_splitter.addWidget(tab_widget)

        # main_splitter.setSizes([1200, 300])
        main_splitter.setStretchFactor(0, 4)
        main_splitter.setStretchFactor(1, 1)
        # init
        self.set_signals()

    def set_signals(self):
        self.filter_le.textChanged.connect(self.set_filter)
        self.send_btn.clicked.connect(self.do_send)
        selection_mode = self.address_tree.selectionModel()
        selection_mode.selectionChanged.connect(self.add_acceptor)

    def set_filter(self, text):
        if text:
            self.address_tree.proxy_model.setFilterRegExp(text)
            self.address_tree.expandAll()
        else:
            self.address_tree.collapseAll()

    def add_acceptor(self, selected, deselected):
        indexes = selected.indexes()
        if not indexes:
            return
        index = indexes[0]
        index = self.address_tree.proxy_model.mapToSource(index)
        node = index.internalPointer()
        if node.node_type == "group":
            users = [child.name() for child in node.children]
        else:
            users = [node.name()]
        current_users = self.acceptor_le.text()
        if not current_users:
            self.acceptor_le.setText(";".join(users))
        else:
            self.acceptor_le.setText("%s;%s" % (current_users, ";".join(users)))

    def do_send(self):
        acceptor_str = self.acceptor_le.text()
        if not acceptor_str:
            QtGui.QMessageBox.information(self, "warming tip", "Please input at least one acceptor.")
            return
        acceptors = acceptor_str.split(";")
        title = self.title_le.text().encode("utf-8")
        content = self.content_te.to_html()
        if not all((acceptors, title, content)):
            QtGui.QMessageBox.information(self, "warming tip", "content missed.")
            return
        current_date = get_current_date.get_current_date()
        sender = getpass.getuser()
        conn = get_redis_conn.get_redis_conn()
        redis_api.send_email(conn, sender, acceptors, title=title, content=content,
                             sender=sender, acceptors=acceptors, send_time=current_date)
        self.pop_message(conn, sender, acceptors, title)

    def pop_message(self, conn, sender, acceptors, title):
        for acceptor in acceptors:
            acceptor_id = conn.get("user:%s:id" % acceptor)
            if acceptor_id is None:
                continue
            acceptor_ip = conn.get("user:%s:ip" % acceptor_id)
            message = "A new email from %s\n%s" % (sender, title)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((acceptor_ip, 1011))
                sock.send(message)
            except:
                print "%s not connected" % acceptor
            finally:
                sock.close()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    se = SendEmailUI()
    se.show()
    app.exec_()
