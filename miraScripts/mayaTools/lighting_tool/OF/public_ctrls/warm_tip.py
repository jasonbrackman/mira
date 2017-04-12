__author__ = 'heshuai'


from PySide import QtGui


def warm_tip(text):
    message_box = QtGui.QMessageBox()
    message_box.setFixedWidth(600)
    message_box.setText('......Warm Tip......')
    message_box.setIcon(QtGui.QMessageBox.Information)
    message_box.setInformativeText(text)
    message_box.exec_()
