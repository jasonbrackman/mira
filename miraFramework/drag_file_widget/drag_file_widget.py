# -*- coding: utf-8 -*-
from Qt.QtWidgets import *

from miraFramework.drag_file_widget.FileListWidget import FileListWidget
from miraFramework.drag_file_widget.press_label import PressLabel


class DragFileWidget(QWidget):
    def __init__(self, parent=None):
        super(DragFileWidget, self).__init__(parent)
        self.stacked_layout = QStackedLayout(self)
        self.press_label = PressLabel()
        self.file_list = FileListWidget()
        self.stacked_layout.addWidget(self.press_label)
        self.stacked_layout.addWidget(self.file_list)
        self.set_signals()
    
    def set_signals(self):
        self.press_label.clicked.connect(self.add_file_to_list)
        
    def add_file_to_list(self, file_list):
        if not file_list:
            return
        for f in file_list:
            self.file_list.add_file_item(f)
        self.stacked_layout.setCurrentIndex(1)


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(DragFileWidget)
