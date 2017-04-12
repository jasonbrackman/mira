#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_style_dec
# description : ''
# author      : HeShuai
# date        : 2016/1/18
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
from PySide import QtGui, QtCore
# Third-party modules

# Studio modules

# Local modules


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_style_dec_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def style_dec(widget_class):

    class StyleClass(widget_class):

        def __init__(self, *args, **kwargs):
            super(StyleClass, self).__init__(*args, **kwargs)
            qss_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "style.qss"))
            if os.path.isfile(qss_path):
                self.setStyle(QtGui.QStyleFactory.create('plastique'))
                self.setStyleSheet(open(qss_path, 'r').read())
            if isinstance(widget_class(), QtGui.QDialog):
                self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    return StyleClass


if __name__ == "__main__":
    pass
