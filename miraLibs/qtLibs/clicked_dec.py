#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/7/21'
# version     :
# usage       :
# notes       :

# Built-in modules
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *

# Third-party modules

# Studio modules

# Local modules


def clicked_dec(widget_class):
    """
    A decorator offers clicked event functions for a qwidget class
    :param widget_class: QObject
    :return MovedClass: QObject
    """

    class ClickedClass(widget_class):
        leftClicked = pyqtSignal()
        rightClicked = pyqtSignal()
        leftDoubleClicked = pyqtSignal()
        rightDoubleClicked = pyqtSignal()

        def __init__(self, *args, **kwargs):
            super(ClickedClass, self).__init__(*args, **kwargs)
            self.wrapped = widget_class()
            self.__timer = QTimer()
            self.__timer.setInterval(250)
            self.__timer.setSingleShot(True)
            self.__timer.timeout.connect(self.timeout)
            self.__left_click_count = self.__right_click_count = 0
            
        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                self.__left_click_count += 1
                if not self.__timer.isActive():
                    self.__timer.start()
            if event.button() == Qt.RightButton:
                self.__right_click_count += 1
                if not self.__timer.isActive():
                    self.__timer.start()
        
        def timeout(self):
            if self.__left_click_count >= self.__right_click_count:
                if self.__left_click_count == 1:
                    self.leftClicked.emit()
                else:
                    self.leftDoubleClicked.emit()
            else:
                if self.__right_click_count == 1:
                    self.rightClicked.emit()
                else:
                    self.rightDoubleClicked.emit()
            self.__left_click_count = self.__right_click_count = 0            

    return ClickedClass

if __name__ == "__main__":
    import sys
    import PyQt4.QtGui as QtGui

    @clicked_dec
    class TestLabel(QLabel):
        pass

    def print_left():
        print "left"
        
    def print_right():
        print "right"
        
    def print_left_double():
        print "left double"
    
    def print_right_double():
        print "right double"

    app = QApplication(sys.argv)
    test = TestLabel("hello")
    test.leftClicked.connect(print_left)
    test.rightClicked.connect(print_right)
    test.leftDoubleClicked.connect(print_left_double)
    test.rightDoubleClicked.connect(print_right_double)
    test.show()
    app.exec_()
