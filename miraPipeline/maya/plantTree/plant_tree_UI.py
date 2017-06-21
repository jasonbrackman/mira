# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\work\plantTree\plantTreeUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *



class plant_tree_UI(QMainWindow):
    def __init__(self,panret=None):
        super(plant_tree_UI,self).__init__(panret)
        self.setupUi(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("plant_tree_mainwindow")
        MainWindow.resize(576, 427)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.treeListWidget = QListWidget(self.groupBox)
        self.treeListWidget.setObjectName("treeListWidget")
        self.gridLayout.addWidget(self.treeListWidget, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.addGroundBtn = QPushButton(self.centralwidget)
        self.addGroundBtn.setObjectName("addGroundBtn")
        self.horizontalLayout.addWidget(self.addGroundBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.startBtn = QPushButton(self.centralwidget)
        self.startBtn.setObjectName("startBtn")
        self.gridLayout_2.addWidget(self.startBtn, 2, 0, 1, 1)
        self.endBtn = QPushButton(self.centralwidget)
        self.endBtn.setObjectName("endBtn")
        self.gridLayout_2.addWidget(self.endBtn, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 576, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("plant tree tool")
        self.groupBox.setTitle("treeList")
        self.label_2.setText("ground")
        self.addGroundBtn.setText( "+")
        self.startBtn.setText( "start")
        self.endBtn.setText("close")

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = plant_tree_UI()
    window.show()

    app.exec_()