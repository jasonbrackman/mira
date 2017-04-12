# -*- coding: utf-8 -*-
import time
import threading
import getpass
from PySide import QtGui, QtCore
from ...libs import redis_api
from . import email_ui
from . import email_model
from ...libs import get_redis_conn


BOX_DICT = {"sendBox": u"已发送", "receiveBox": u"收件箱", "recycleBox": u"回收站"}


class EmailBox(email_ui.EmailUI):
    def __init__(self, box=None, parent=None):
        super(EmailBox, self).__init__(parent)
        self.box = box
        self.box_label.setText("<font size=5><b>%s</b></font>" % BOX_DICT.get(self.box))
        self.user = getpass.getuser()
        self.conn = get_redis_conn.get_redis_conn()
        self.model = None
        self.set_model()
        self.set_signals()
        if self.box == "receiveBox":
            t = threading.Thread(target=self.collect_unread_emails)
            t.setDaemon(True)
            t.start()

    def set_model(self):
        self.email_model_data = redis_api.get_receive_emails(self.conn, self.user, self.box)
        self.proxy_model = QtGui.QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        if not self.email_model_data:
            return
        self.model = email_model.EmailListModel(self.email_model_data, self.box, self)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(0)
        self.email_list_view.setModel(self.proxy_model)

    def set_signals(self):
        self.email_list_view.clicked.connect(self.on_email_clicked)
        self.delete_action.triggered.connect(self.delete_email)
        self.filter_le.textChanged.connect(self.set_filter)

    def set_filter(self, text):
        self.proxy_model.setFilterRegExp(text)

    def show_email(self, row):
        current_email_item = self.model.arg[row]
        content = current_email_item.content.decode("utf-8")
        self.content_text.setHtml(content)
        # set title
        email_title = current_email_item.title.decode("utf8")
        self.title_label.setText("<font size=4><b>Title: %s</b></font>" % email_title)
        return current_email_item

    def on_email_clicked(self, index):
        source_index = self.proxy_model.mapToSource(index)
        self.model.clicked_indexes.append(source_index)
        row = source_index.row()
        current_email_item = self.show_email(row)
        # change current email read
        if self.box == "receiveBox":
            email_id = int(current_email_item.email_id)
            self.conn.set("email:%s:isReadBy%s" % (email_id, self.user), 1)

    def get_selected_rows(self):
        selected_indexes = self.email_list_view.selectedIndexes()
        if not selected_indexes:
            return
        rows = list()
        for index in selected_indexes:
            rows.append(self.proxy_model.mapToSource(index).row())
        return rows

    def delete_email(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            return
        selected_rows.sort()
        # delete from database
        email_id_list = [self.model.arg[row].email_id for row in selected_rows]
        redis_api.delete_email(self.conn, self.user, email_id_list, self.box)
        # delete from model
        for index, row in enumerate(selected_rows):
            self.model.removeRows(row-index, 1)
        # set current display
        try:
            self.show_email(0)
        except:
            self.content_text.setText("")
            self.title_label.setText("")

    def collect_unread_emails(self):
        if self.box == "receiveBox":
            while 1:
                if self.model is None:
                    continue
                email_ids = [email.email_id for email in self.model.arg]
                time.sleep(1)
                unread_emails = redis_api.get_unread_emails(self.conn)
                if not unread_emails:
                    continue
                for email in unread_emails:
                    if email.email_id not in email_ids:
                        self.model.insertRows(0, 1, [email])
