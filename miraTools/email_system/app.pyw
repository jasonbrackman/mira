# -*- coding: utf-8 -*-
import time
import subprocess
import socket
import sys
import threading
import getpass
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from python.ui import system_tray
from python.ui import email_system_ui
from python.libs import get_redis_conn, get_local_ip, redis_api


class EmailSystem(object):
    def __init__(self):
        self.threads = list()
        self.app = QApplication(sys.argv)
        self.tray = system_tray.SystemTray(self.app)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = get_local_ip.get_local_ip()
        self.port = 1011
        self.conn = get_redis_conn.get_redis_conn()
        self.init_user()

    def open_port(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        while True:
            try:
                conn, addr = self.sock.accept()
                command = conn.recv(2048)
                if command:
                    self.tray.show_message(msg=command.decode("utf-8"))
                    try:
                        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    except:
                        pass
            except KeyboardInterrupt:
                print "exit"
                sys.exit(0)

    def show_system_tray_icon(self):
        QApplication.setQuitOnLastWindowClosed(False)
        self.tray.quit_action.triggered.connect(self.quit)
        self.tray.activated.connect(self.on_tray_double_clicked)
        self.tray.messageClicked.connect(self.show_email)
        self.tray.show()
        self.app.exec_()

    def quit(self):
        self.tray.deleteLater()
        self.sock.close()
        self.app.quit()

    def start(self):
        # check port is using
        check_sock = socket.socket()
        port_is_using = check_sock.connect_ex((self.host, self.port))
        if not port_is_using:
            check_sock.close()
            return
        # open port
        open_port_thread = threading.Thread(target=self.open_port)
        show_unread_email_thread = threading.Thread(target=self.show_unread_emails)
        self.threads.append(open_port_thread)
        self.threads.append(show_unread_email_thread)
        open_port_thread.setDaemon(True)
        show_unread_email_thread.setDaemon(True)
        open_port_thread.start()
        show_unread_email_thread.start()
        self.show_system_tray_icon()

    def on_tray_double_clicked(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_email()

    def show_email(self):
        global send_ui
        try:
            send_ui.deleteLater()
        except:pass
        send_ui = email_system_ui.EmailSystemUI()
        send_ui.activateWindow()
        send_ui.raise_()
        send_ui.show()

    def init_user(self):
        user = getpass.getuser()
        redis_api.add_user(self.conn, user, ip=self.host)

    def show_unread_emails(self):
        time.sleep(3)
        unread_emails = redis_api.get_unread_emails(self.conn)
        if unread_emails:
            self.tray.show_message(msg=u"你有%s封未读邮件" % len(unread_emails))


def main():
    es = EmailSystem()
    es.start()


if __name__ == "__main__":
    main()
