# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *


class PressLabel(QLabel):
    clicked = Signal(list)

    def __init__(self, parent=None):
        super(PressLabel, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setText("Drag and drop files here or clicked to browse")
        self.set_style()

    def set_style(self):
        self.setStyleSheet("QLabel{padding: 3px;border: 2px dashed #666666;border-radius:10px;"
                           "font: bold 16px/25px Arial, sans-serif;color:#666666;qproperty-alignment: AlignCenter;}"
                           "QLabel:hover{border-color:#2194c4;color:#2194c4}")

    def mousePressEvent(self, event):
        file_dialog = QFileDialog.getOpenFileNames(self)
        file_list = file_dialog[0]
        self.clicked.emit(file_list)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        paths = list()
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            paths.append(path)
        self.clicked.emit(paths)


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(DragLabel)
