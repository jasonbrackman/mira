__author__ = 'heshuai'


from PySide import QtGui


def set_btn_text_color(btn, color):
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ButtonText, color)
    btn.setPalette(palette)