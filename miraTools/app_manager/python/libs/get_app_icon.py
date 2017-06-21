# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


def get_app_icon(path):
    file_info = QFileInfo(path)
    icon_provider = QFileIconProvider()
    icon = icon_provider.icon(file_info)
    return icon
