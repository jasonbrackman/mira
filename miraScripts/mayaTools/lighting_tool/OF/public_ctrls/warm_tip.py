__author__ = 'heshuai'


from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


def warm_tip(text):
    message_box = QMessageBox()
    message_box.setFixedWidth(600)
    message_box.setText('......Warm Tip......')
    message_box.setIcon(QMessageBox.Information)
    message_box.setInformativeText(text)
    message_box.exec_()
