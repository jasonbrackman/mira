# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


def get(content):
    settings = QSettings("Mira", "History")
    return settings.value(content)


def set(key, value):
    settings = QSettings("Mira", "History")
    settings.setValue(key, value)
