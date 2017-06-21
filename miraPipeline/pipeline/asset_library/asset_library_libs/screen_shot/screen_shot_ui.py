# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import resource


class Ui_ThumbnailWidget(object):
    def setupUi(self, ThumbnailWidget):
        ThumbnailWidget.setObjectName("ThumbnailWidget")
        ThumbnailWidget.resize(347, 266)
        ThumbnailWidget.setStyleSheet("")
        self.thumbnail = QLabel(ThumbnailWidget)
        self.thumbnail.setGeometry(QRect(210, 190, 81, 61))
        self.thumbnail.setMinimumSize(QSize(0, 0))
        self.thumbnail.setMaximumSize(QSize(16777215, 16777215))
        self.thumbnail.setStyleSheet("")
        self.thumbnail.setText("")
        self.thumbnail.setScaledContents(False)
        self.thumbnail.setAlignment(Qt.AlignCenter)
        self.thumbnail.setObjectName("thumbnail")
        self.buttons_frame = QFrame(ThumbnailWidget)
        self.buttons_frame.setGeometry(QRect(40, 30, 211, 191))
        self.buttons_frame.setStyleSheet("#buttons_frame {\n"
"border-radius: 2px;\n"
"background-color: rgba(0,0,0, 64);\n"
"}")
        self.buttons_frame.setFrameShape(QFrame.NoFrame)
        self.buttons_frame.setFrameShadow(QFrame.Plain)
        self.buttons_frame.setLineWidth(0)
        self.buttons_frame.setObjectName("buttons_frame")
        self.verticalLayout_2 = QVBoxLayout(self.buttons_frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QSpacerItem(20, 52, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.camera_btn = QPushButton(self.buttons_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_btn.sizePolicy().hasHeightForWidth())
        self.camera_btn.setSizePolicy(sizePolicy)
        self.camera_btn.setMinimumSize(QSize(64, 64))
        self.camera_btn.setMaximumSize(QSize(16777215, 16777215))
        self.camera_btn.setCursor(Qt.PointingHandCursor)
        self.camera_btn.setStyleSheet("#camera_btn {\n"
"    background-color: rgba( 0, 0, 0, 0 );\n"
"    image: url(:/images/camera.png);\n"
"    margin: 5px;\n"
"    border: none;\n"
"}\n"
"#camera_btn:hover {\n"
"    image: url(:/images/camera_hl.png);\n"
"}\n"
"#camera_btn:focus:pressed {\n"
"    image: url(:/images/camera_hl.png);\n"
"}\n"
"\n"
"")
        self.camera_btn.setText("")
        self.camera_btn.setIconSize(QSize(64, 64))
        self.camera_btn.setFlat(True)
        self.camera_btn.setObjectName("camera_btn")
        self.horizontalLayout_2.addWidget(self.camera_btn)
        spacerItem2 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem3 = QSpacerItem(20, 51, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(2, 1)

        self.retranslateUi(ThumbnailWidget)
        QMetaObject.connectSlotsByName(ThumbnailWidget)

    def retranslateUi(self, ThumbnailWidget):
        try:
            ThumbnailWidget.setWindowTitle(QApplication.translate("ThumbnailWidget", "Screen Shot", None, QApplication.UnicodeUTF8))
        except:
            ThumbnailWidget.setWindowTitle(QApplication.translate("ThumbnailWidget", "Screen Shot", None))

if __name__ == "__main__":
    pass
