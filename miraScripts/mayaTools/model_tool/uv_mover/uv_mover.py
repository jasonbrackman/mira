# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uv_mover.ui'
#
# Created: Wed Mar 16 19:06:36 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_UVMover(object):
    def setupUi(self, UVMover):
        UVMover.setObjectName("UVMover")
        UVMover.resize(194, 210)
        self.verticalLayout = QtGui.QVBoxLayout(UVMover)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.l_up_btn = QtGui.QToolButton(UVMover)
        self.l_up_btn.setMinimumSize(QtCore.QSize(50, 50))
        self.l_up_btn.setMaximumSize(QtCore.QSize(50, 50))
        self.l_up_btn.setObjectName("l_up_btn")
        self.gridLayout.addWidget(self.l_up_btn, 0, 0, 1, 1)
        self.up_btn = QtGui.QToolButton(UVMover)
        self.up_btn.setMinimumSize(QtCore.QSize(50, 50))
        self.up_btn.setMaximumSize(QtCore.QSize(50, 50))
        self.up_btn.setObjectName("up_btn")
        self.gridLayout.addWidget(self.up_btn, 0, 1, 1, 1)
        self.r_up_btn = QtGui.QToolButton(UVMover)
        self.r_up_btn.setMinimumSize(QtCore.QSize(50, 50))
        self.r_up_btn.setMaximumSize(QtCore.QSize(50, 50))
        self.r_up_btn.setObjectName("r_up_btn")
        self.gridLayout.addWidget(self.r_up_btn, 0, 2, 1, 1)
        self.left_btn = QtGui.QToolButton(UVMover)
        self.left_btn.setMinimumSize(QtCore.QSize(50, 50))
        self.left_btn.setMaximumSize(QtCore.QSize(50, 50))
        self.left_btn.setObjectName("left_btn")
        self.gridLayout.addWidget(self.left_btn, 1, 0, 1, 1)
        self.right_btn = QtGui.QToolButton(UVMover)
        self.right_btn.setMinimumSize(QtCore.QSize(50, 50))
        self.right_btn.setMaximumSize(QtCore.QSize(50, 50))
        self.right_btn.setObjectName("right_btn")
        self.gridLayout.addWidget(self.right_btn, 1, 2, 1, 1)
        self.l_down_btn = QtGui.QToolButton(UVMover)
        self.l_down_btn.setMinimumSize(QtCore.QSize(50, 50))
        self.l_down_btn.setMaximumSize(QtCore.QSize(50, 50))
        self.l_down_btn.setObjectName("l_down_btn")
        self.gridLayout.addWidget(self.l_down_btn, 2, 0, 1, 1)
        self.down_btn = QtGui.QToolButton(UVMover)
        self.down_btn.setMinimumSize(QtCore.QSize(50, 50))
        self.down_btn.setMaximumSize(QtCore.QSize(50, 50))
        self.down_btn.setObjectName("down_btn")
        self.gridLayout.addWidget(self.down_btn, 2, 1, 1, 1)
        self.r_down_btn = QtGui.QToolButton(UVMover)
        self.r_down_btn.setMinimumSize(QtCore.QSize(50, 50))
        self.r_down_btn.setMaximumSize(QtCore.QSize(50, 50))
        self.r_down_btn.setObjectName("r_down_btn")
        self.gridLayout.addWidget(self.r_down_btn, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout.setStretch(0, 10)

        self.retranslateUi(UVMover)
        QtCore.QObject.connect(self.l_up_btn, QtCore.SIGNAL("clicked()"), UVMover.do_move_uv)
        QtCore.QObject.connect(self.up_btn, QtCore.SIGNAL("clicked()"), UVMover.do_move_uv)
        QtCore.QObject.connect(self.r_up_btn, QtCore.SIGNAL("clicked()"), UVMover.do_move_uv)
        QtCore.QObject.connect(self.left_btn, QtCore.SIGNAL("clicked()"), UVMover.do_move_uv)
        QtCore.QObject.connect(self.right_btn, QtCore.SIGNAL("clicked()"), UVMover.do_move_uv)
        QtCore.QObject.connect(self.l_down_btn, QtCore.SIGNAL("clicked()"), UVMover.do_move_uv)
        QtCore.QObject.connect(self.down_btn, QtCore.SIGNAL("clicked()"), UVMover.do_move_uv)
        QtCore.QObject.connect(self.r_down_btn, QtCore.SIGNAL("clicked()"), UVMover.do_move_uv)
        QtCore.QMetaObject.connectSlotsByName(UVMover)

    def retranslateUi(self, UVMover):
        UVMover.setWindowTitle(QtGui.QApplication.translate("UVMover", "UV Mover", None, QtGui.QApplication.UnicodeUTF8))
        self.l_up_btn.setText(QtGui.QApplication.translate("UVMover", "↖", None, QtGui.QApplication.UnicodeUTF8))
        self.up_btn.setText(QtGui.QApplication.translate("UVMover", "↑", None, QtGui.QApplication.UnicodeUTF8))
        self.r_up_btn.setText(QtGui.QApplication.translate("UVMover", "↗", None, QtGui.QApplication.UnicodeUTF8))
        self.left_btn.setText(QtGui.QApplication.translate("UVMover", "←", None, QtGui.QApplication.UnicodeUTF8))
        self.right_btn.setText(QtGui.QApplication.translate("UVMover", "→", None, QtGui.QApplication.UnicodeUTF8))
        self.l_down_btn.setText(QtGui.QApplication.translate("UVMover", "↙", None, QtGui.QApplication.UnicodeUTF8))
        self.down_btn.setText(QtGui.QApplication.translate("UVMover", "↓", None, QtGui.QApplication.UnicodeUTF8))
        self.r_down_btn.setText(QtGui.QApplication.translate("UVMover", "↘", None, QtGui.QApplication.UnicodeUTF8))

