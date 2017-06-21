# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from input import Input
import output
reload(output)
from output import Output
from asset_library_libs.get_engine import get_engine


class Assetlibrary(QDialog):
    def __init__(self, parent=None):
        super(Assetlibrary, self).__init__(parent)
        self.setObjectName("AssetLibrary")
        self.setWindowTitle("AssetLibrary")
        self.resize(380, 600)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        tab_widget = QTabWidget()
        tab_widget.setTabPosition(QTabWidget.West)

        input_library = Input()
        output_library = Output()
        tab_widget.addTab(input_library, "Input")
        tab_widget.addTab(output_library, "Output")

        main_layout.addWidget(tab_widget)


def show_in_maya():
    from miraLibs.mayaLibs import show_as_panel
    show_as_panel.show_as_panel(Assetlibrary())


def main():
    engine = get_engine()
    if engine == "maya":
        show_in_maya()
