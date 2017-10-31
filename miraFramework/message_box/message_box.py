import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


COLOR_DICT = {"Error": "#FF0000", "Warning": "#ffff33", "Success": "#00FF00"}


class MessageWidget(QDialog):
    def __init__(self, title=None, label=None, parent=None):
        super(MessageWidget, self).__init__(parent)
        self.title = title
        self.label = label
        self.setup_ui()
        self.show_content()
        self.setStyleSheet("background-color: #FFFFFF")

    def setup_ui(self):
        self.setWindowFlags(Qt.Popup)
        main_layout = QVBoxLayout(self)
        self.setFixedSize(300, 300)
        self.title_label = QLabel()
        self.setMinimumHeight(80)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setMinimumHeight(50)
        self.label_label = QLabel()
        self.label_label.setWordWrap(True)
        self.label_label.setAlignment(Qt.AlignTop)
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.label_label)
        main_layout.addStretch()
        main_layout.addWidget(self.icon_label)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addStretch()
        main_layout.setSpacing(20)

    def get_icon(self):
        icon_path = os.path.abspath(os.path.join(__file__, "..", "icons", "%s.png" % self.title))
        return icon_path

    def show_content(self):
        title_color = COLOR_DICT.get(self.title)
        icon_path = self.get_icon()
        self.title_label.setText("<font face=Arial Black color=%s size=15><b>%s</b></font>" % (title_color, self.title))
        self.label_label.setText("<font face=Arial Black color=#000 size=4>%s</font>" % self.label)
        pix_map = QPixmap(icon_path)
        scaled = pix_map.scaled(self.width(), 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled)


if __name__ == "__main__":
    MessageWidget("Error", "test")