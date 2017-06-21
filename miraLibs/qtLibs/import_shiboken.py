# -*- coding: utf-8 -*-
from Qt import __binding__


if __binding__ in ["PySide2", "PyQt5"]:
    import shiboken2 as shiboken
elif __binding__ in ["PySide", "PyQt4"]:
    import shiboken
