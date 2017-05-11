# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\work\mira\miraScripts\mayaTools\camera_sequencer\camera_sequencer_UI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class camera_sequencer_UI(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(camera_sequencer_UI,self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(576, 375)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.multiGroupBox = QtGui.QGroupBox(self.centralwidget)
        self.multiGroupBox.setObjectName("multiGroupBox")
        self.gridLayout = QtGui.QGridLayout(self.multiGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.shotListWidget = QtGui.QListWidget(self.multiGroupBox)
        self.shotListWidget.setObjectName("shotListWidget")
        self.gridLayout.addWidget(self.shotListWidget, 0, 0, 1, 1)
        self.multiCamCreateBtn = QtGui.QPushButton(self.multiGroupBox)
        self.multiCamCreateBtn.setMinimumSize(QtCore.QSize(0, 30))
        self.multiCamCreateBtn.setObjectName("multiCamCreateBtn")
        self.gridLayout.addWidget(self.multiCamCreateBtn, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.multiGroupBox, 1, 0, 1, 2)
        self.deleteAllBtn = QtGui.QPushButton(self.centralwidget)
        self.deleteAllBtn.setMinimumSize(QtCore.QSize(0, 50))
        self.deleteAllBtn.setObjectName("deleteAllBtn")
        self.gridLayout_2.addWidget(self.deleteAllBtn, 2, 0, 1, 1)
        self.closeBtn = QtGui.QPushButton(self.centralwidget)
        self.closeBtn.setMinimumSize(QtCore.QSize(0, 50))
        self.closeBtn.setObjectName("closeBtn")
        self.gridLayout_2.addWidget(self.closeBtn, 2, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sceneNameLabel = QtGui.QLabel(self.centralwidget)
        self.sceneNameLabel.setObjectName("sceneNameLabel")
        self.horizontalLayout.addWidget(self.sceneNameLabel)
        self.sceneNameLineEdit = QtGui.QLineEdit(self.centralwidget)
        self.sceneNameLineEdit.setObjectName("sceneNameLineEdit")
        self.horizontalLayout.addWidget(self.sceneNameLineEdit)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 576, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        self.multiGroupBox.setTitle("create multiply sequence")
        self.multiCamCreateBtn.setText("create")
        self.deleteAllBtn.setText( "deleteAll")
        self.closeBtn.setText("close")
        self.sceneNameLabel.setText( "current scene")

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = camera_sequencer_UI()
    window.show()

    app.exec_()