# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from camera_sequencer_UI import camera_sequencer_UI
from miraLibs.mayaLibs import get_maya_win
from miraLibs.pipeLibs.pipeDb import sql_api
import maya.cmds as mc


class CameraSequencer(camera_sequencer_UI):
    def __init__(self, parent=None):
        super(CameraSequencer, self).__init__(parent)
        self.set_additional()
        self.make_connections()

    def set_additional(self):
        self.setFixedHeight(543)
        self.setFixedWidth(300)
        self.setWindowTitle('Camera Sequencer')
        self.set_scene_name()

        self.shotListWidget.setSelectionMode(QAbstractItemView.NoSelection)

    def set_scene_name(self):
        full_scene_name = mc.file(q=True, sceneName=True)
        if full_scene_name == '':
            return
        scene_name_list = full_scene_name.split('/')[-1].split('.')[0].split('_')
        project_name = scene_name_list[0]
        scene_name = scene_name_list[1]
        self.sceneNameLineEdit.setText(scene_name)
        shot_list = sql_api.SqlApi(project_name).getShotListBySceneName({'assetScene':scene_name})
        for i in shot_list:
            item = QListWidgetItem()
            item.setText(scene_name+'_'+i)
            self.shotListWidget.addItem(item)

    def make_connections(self):
        self.multiCamCreateBtn.clicked.connect(self.create_multi_sequence)
        self.deleteAllBtn.clicked.connect(self.delete_all)
        self.closeBtn.clicked.connect(self.close)

    def create_multi_sequence(self):
        if not self.judge_scene_name():
            QMessageBox.information(self, 'error', 'please input a scene name')
            return
        shot_list_count = self.shotListWidget.count()
        for i in range(shot_list_count):
            shot_name = self.shotListWidget.item(i).text()
            self.do_create_sequence(shot_name)
        QMessageBox.information(self, 'success', 'create complete')

    def do_create_sequence(self, shot_name):
        camera_name = 'cam_%s' % shot_name
        shot_name = 'shot_%s' % shot_name
        if mc.objExists(camera_name):
            QMessageBox.information(self, 'error', '%s exists' % camera_name)
            return
        new_cam = mc.camera()
        mc.setAttr(new_cam[1]+'.filmFit', 1)
        mc.parent(new_cam[0], 'camera')
        mc.rename(mc.ls(sl=True)[0], camera_name)
        mc.rename(mc.listRelatives(mc.ls(sl=True)[0], c=1, shapes=1)[0], camera_name+'Shape')
        mc.shot(shot_name, currentCamera=camera_name)

    def judge_scene_name(self):
        if self.sceneNameLineEdit.text() == '':
            return False
        return True

    def delete_all(self):
        ask = QMessageBox.information(self, 'Question', 'Are you sure delete all shot camera and shot ?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ask == QMessageBox.Yes:
            if mc.listRelatives('camera', c=1):
                for i in mc.listRelatives('camera', c=1):
                    mc.delete(i)
            for i in mc.ls(type='shot'):
                mc.delete(i)
        else:
            return


def main():
    maya_win = get_maya_win.get_maya_win("PySide")
    window = CameraSequencer(maya_win)
    window.show()
    
    
if __name__ == '__main__':
    main()
    
