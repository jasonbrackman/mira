# -*- coding: utf-8 -*-
import logging
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.backup import backup
from miraLibs.pipeLibs import pipeMira
from miraLibs.pyLibs import join_path
from miraLibs.mayaLibs import get_maya_win


logger = logging.getLogger(__name__)


class Maya(object):
    def __init__(self):
        obj = pipeFile.PathDetails.parse_path()
        self.seq = obj.seq
        self.project = obj.project
        self.camera_path = obj.camera_path
        self.preAnim_dir = obj.preAnim_dir

    @staticmethod
    def get_shot_nodes():
        shots = mc.ls(type="shot")
        return shots

    def export_cameras(self):
        sequencer = "sequencer_%s" % self.seq
        if not mc.objExists(sequencer):
            logger.error("%s does not exist." % sequencer)
            return
        mc.select(clear=1)
        mc.select(sequencer, r=1)
        mc.file(self.camera_path, exportSelected=1, type="mayaBinary", f=1, options="v=0", preserveReferences=1)
        logger.info("Export camera to %s" % self.camera_path)
        backup.backup(self.project, self.camera_path)

    def create_anim_file(self, shot):
        shot_name = shot.split("_")[-1]
        file_base_name = pipeMira.get_shot_file_name(self.project)
        file_name = file_base_name.format(project_name=self.project, sequence=self.seq, shot=shot_name,
                                          category="anim", version="000")
        anim_file = join_path.join_path2(self.preAnim_dir, file_name)
        mc.select(clear=1)
        select_groups = ["sceneset", "prop", "char", "_REF", shot]
        mc.select(select_groups, r=1)
        mc.file(anim_file, exportSelected=1, type="mayaBinary", f=1, options="v=0", preserveReferences=1)
        logger.info("Create pre animation file: %s" % anim_file)


class PublishSingleLay(QDialog):
    def __init__(self, parent=None):
        super(PublishSingleLay, self).__init__(parent)
        self.setWindowTitle("Publish Single Lay Shot")
        self.setObjectName("Publish Single Lay Shot")
        self.resize(400, 250)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 3, 0, 5)
        self.shot_lw = QListWidget()
        self.shot_lw.setSortingEnabled(True)
        btn_layout = QHBoxLayout()
        self.publish_btn = QPushButton("publish")
        self.close_btn = QPushButton("close")
        btn_layout.addStretch()
        btn_layout.addWidget(self.publish_btn)
        btn_layout.addWidget(self.close_btn)
        main_layout.addWidget(self.shot_lw)
        main_layout.addLayout(btn_layout)

        self.maya = Maya()
        self.add_shots()
        self.set_signals()

    def set_signals(self):
        self.publish_btn.clicked.connect(self.do_publish)
        self.close_btn.clicked.connect(self.close)

    def add_shots(self):
        shot_nodes = self.maya.get_shot_nodes()
        if shot_nodes:
            self.shot_lw.addItems(shot_nodes)

    def get_selected(self):
        selected_items = self.shot_lw.selectedItems()
        if not selected_items:
            return
        selected_shots = [item.text() for item in selected_items]
        return selected_shots

    def do_publish(self):
        selected_shots = self.get_selected()
        if not selected_shots:
            return
        self.maya.export_cameras()
        for shot in selected_shots:
            self.maya.create_anim_file(shot)


def main():
    if mc.window("Publish Single Lay Shot", q=1, ex=1):
        mc.deleteUI("Publish Single Lay Shot")
    psl = PublishSingleLay(get_maya_win.get_maya_win("PySide"))
    psl.show()


if __name__ == "__main__":
    main()
