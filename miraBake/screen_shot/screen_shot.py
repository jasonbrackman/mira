# -*- coding: utf-8 -*-
import logging
import os
import shutil
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraLibs.pipeLibs import pipeFile
from miraFramework.screen_shot import screen_shot
from miraLibs.mayaLibs import get_maya_win
from miraLibs.pipeLibs.backup import backup


class ScreenShot(QDialog):
    def __init__(self, parent=None):
        super(ScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle("Screen Shot")
        self.resize(400, 300)
        main_layout = QVBoxLayout(self)
        self.screen_shot_widget = screen_shot.ThumbnailWidget()
        main_layout.addWidget(self.screen_shot_widget)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(btn_layout)
        self.set_signals()

    def set_signals(self):
        self.save_btn.clicked.connect(self.save_pixmap)
        self.cancel_btn.clicked.connect(self.close)

    def save_pixmap(self):
        logger = logging.getLogger(__name__)
        pix_map = self.screen_shot_widget.get_thumbnail_path()
        obj = pipeFile.PathDetails.parse_path()
        current_project = obj.project
        work_path = obj.work_path
        image_path = pipeFile.get_path(work_path, "_QCPublish", ".png", "0")
        backup.backup(current_project, image_path)
        if not os.path.isdir(os.path.dirname(image_path)):
            os.makedirs(os.path.dirname(image_path))
        shutil.copy(pix_map, image_path)
        logger.info("copy %s ---> %s" % (pix_map, image_path))
        os.remove(pix_map)
        logger.info("Screen shot successful.")
        self.close()


def main():
    ss = ScreenShot(get_maya_win.get_maya_win("PySide"))
    ss.show()
