# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from ..libs import get_icon_path


class SearchLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(SearchLineEdit, self).__init__(parent)
        self.setPlaceholderText("Search the app you want.")
        self.button = QToolButton(self)
        self.button.setEnabled(False)
        icon = QIcon(get_icon_path.get_icon_path("search.png"))
        self.button.setIcon(icon)
        self.button.setStyleSheet("QToolButton{border: 0px; padding: 0px; background:transparent}"\
                                  "QToolButton::hover{background:transparent}")
        self.button.setCursor(Qt.ArrowCursor)
        self.button.clicked.connect(self.editingFinished)

        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        button_size = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (button_size.width() + frame_width + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), button_size.width() + frame_width*2 + 2),
                            max(self.minimumSizeHint().height(), button_size.height() + frame_width*2 + 2))

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frame_width - button_size.width(),
                         (self.rect().bottom() - button_size.height() + 1)/2)
        super(SearchLineEdit, self).resizeEvent(event)

    def set_completer(self, completer_list):
        completer = QCompleter(completer_list)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(completer)


if __name__ == "__main__":
    pass
