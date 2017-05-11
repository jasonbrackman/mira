# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reset_dialog.ui'
#
# Created: Mon Jan 25 15:28:19 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_reset_dlg(object):
    def setupUi(self, reset_dlg):
        reset_dlg.setObjectName("reset_dlg")
        reset_dlg.resize(389, 99)
        self.verticalLayout = QtGui.QVBoxLayout(reset_dlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.info_label_1 = QtGui.QLabel(reset_dlg)
        self.info_label_1.setObjectName("info_label_1")
        self.horizontalLayout.addWidget(self.info_label_1)
        self.duration_spin = QtGui.QSpinBox(reset_dlg)
        self.duration_spin.setMinimum(20)
        self.duration_spin.setMaximum(120)
        self.duration_spin.setSingleStep(20)
        self.duration_spin.setProperty("value", 20)
        self.duration_spin.setObjectName("duration_spin")
        self.horizontalLayout.addWidget(self.duration_spin)
        self.info_label_2 = QtGui.QLabel(reset_dlg)
        self.info_label_2.setObjectName("info_label_2")
        self.horizontalLayout.addWidget(self.info_label_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.info_label_3 = QtGui.QLabel(reset_dlg)
        self.info_label_3.setObjectName("info_label_3")
        self.horizontalLayout_3.addWidget(self.info_label_3)
        self.duration_label = QtGui.QLabel(reset_dlg)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.duration_label.setFont(font)
        self.duration_label.setObjectName("duration_label")
        self.horizontalLayout_3.addWidget(self.duration_label)
        self.label_5 = QtGui.QLabel(reset_dlg)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.cancel_btn = QtGui.QPushButton(reset_dlg)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_2.addWidget(self.cancel_btn)
        self.ok_btn = QtGui.QPushButton(reset_dlg)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout_2.addWidget(self.ok_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(reset_dlg)
        QtCore.QObject.connect(self.duration_spin, QtCore.SIGNAL("valueChanged(QString)"), self.duration_label.setText)
        QtCore.QObject.connect(self.cancel_btn, QtCore.SIGNAL("clicked()"), reset_dlg.close)
        QtCore.QObject.connect(self.ok_btn, QtCore.SIGNAL("clicked()"), reset_dlg.close)
        QtCore.QMetaObject.connectSlotsByName(reset_dlg)

    def retranslateUi(self, reset_dlg):
        reset_dlg.setWindowTitle(QtGui.QApplication.translate("reset_dlg", "设置保存提醒时间间隔", None, QtGui.QApplication.UnicodeUTF8))
        self.info_label_1.setText(QtGui.QApplication.translate("reset_dlg", "设置保存提醒间隔时间为", None, QtGui.QApplication.UnicodeUTF8))
        self.info_label_2.setText(QtGui.QApplication.translate("reset_dlg", "分钟", None, QtGui.QApplication.UnicodeUTF8))
        self.info_label_3.setText(QtGui.QApplication.translate("reset_dlg", "Notice message will raise every", None, QtGui.QApplication.UnicodeUTF8))
        self.duration_label.setText(QtGui.QApplication.translate("reset_dlg", "20", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("reset_dlg", "Minutes", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_btn.setText(QtGui.QApplication.translate("reset_dlg", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_btn.setText(QtGui.QApplication.translate("reset_dlg", "OK", None, QtGui.QApplication.UnicodeUTF8))

