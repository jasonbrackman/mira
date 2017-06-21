__author__ = 'heshuai'


from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


def set_btn_text_color(btn, color):
    palette = QPalette()
    palette.setColor(QPalette.ButtonText, color)
    btn.setPalette(palette)