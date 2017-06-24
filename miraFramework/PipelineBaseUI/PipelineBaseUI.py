import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *

BACKGROUND_ICON_PATH = os.path.join(os.path.dirname(__file__), "title.png").replace("\\", "/")
ICON_PATH = os.path.join(os.path.dirname(__file__), "smile.png").replace("\\", "/")
TITLE_HEIGHT = 45


class HasBackgroundWidget(QWidget):
    def __init__(self, image_path, parent=None):
        super(HasBackgroundWidget, self).__init__(parent)
        self.image_path = image_path
        self.set_background()

    def set_background(self):
        self.image = QImage()
        self.image.load(self.image_path)
        self.setAutoFillBackground(True)
        self.set_palette()

    def set_palette(self):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.image.scaled(self.width(), self.height(),
                                                                                   Qt.KeepAspectRatio,
                                                                                   Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_palette()


class BackgroundWidget(HasBackgroundWidget):
    def __init__(self, image_path, parent=None):
        super(BackgroundWidget, self).__init__(image_path, parent)
        self.setFixedHeight(TITLE_HEIGHT)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.icon_label = QLabel()
        self.icon_label.setAutoFillBackground(True)
        self.icon_label.setFixedSize(self.height(), self.height())
        self.text_label = QLabel()
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.text_label)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
        self.set_icon_label()

    def set_icon_label(self):
        pix_map = QPixmap(ICON_PATH)
        scaled = pix_map.scaled(QSize(self.icon_label.width(), self.icon_label.height()),
                                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled)


class PipelineBaseUI(QDialog):
    def __init__(self, widget_class, parent=None):
        super(PipelineBaseUI, self).__init__(parent)
        self.setObjectName("PipelineBaseUI")
        self.widget = widget_class()
        window_title = self.widget.windowTitle()
        self.setWindowTitle(window_title)
        self.resize(self.widget.width(), self.widget.height()+TITLE_HEIGHT)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setWindowFlags(self.widget.windowFlags())
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.main_layout.setAlignment(Qt.AlignTop)
        self.background_widget = BackgroundWidget(BACKGROUND_ICON_PATH)
        self.label = self.background_widget.text_label
        self.label.setText('<font face="Microsoft YaHei" color="#FFFFFF" size=6>%s</font>' % window_title)
        self.main_layout.addWidget(self.background_widget)
        self.main_layout.addWidget(self.widget)
