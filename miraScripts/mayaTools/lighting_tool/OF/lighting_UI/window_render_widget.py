import logging
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import maya.mel as mel
from miraLibs.mayaLibs import get_maya_win
from miraLibs.pyLibs import get_range_data


class MayaUtility(object):
    def render(self, layers, camera, frames):
        mel.eval('$gRenderViewRenderAborted = 0')
        mel.eval('proc int Aborted(){global int $gRenderViewRenderAborted;return $gRenderViewRenderAborted;}')
        mc.RenderViewWindow()
        for layer in layers:
            mc.editRenderLayerGlobals(currentRenderLayer=layer)
            for frame in frames:
                mc.currentTime(frame)
                mel.eval('renderWindowRenderCamera render renderView ' + camera)
                if mel.eval('Aborted'):
                    break
            if mel.eval('Aborted'):
                break

    def get_render_layer(self, value=None):
        if not value:
            render_layers = [mc.editRenderLayerGlobals(q=1, currentRenderLayer=1)]
        else:
            render_layers = mc.ls(type='renderLayer')
            render_layers = [layer for layer in render_layers if 'defaultRenderLayer' not in layer]
            render_layers = [layer for layer in render_layers if mc.getAttr('%s.renderable' % layer)]
        return render_layers

    def get_camera(self):
        cameras = mc.ls(cameras=1)
        return cameras


class FRenderView(QDialog):
    utility = MayaUtility()

    def __init__(self, parent=None):
        super(FRenderView, self).__init__(parent)
        self.setObjectName('Foreground Render')
        self.setWindowTitle('Foreground Render')
        self.resize(400, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setWindowFlags(Qt.Dialog | Qt.WindowMinimizeButtonHint)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)

        check_layout = QHBoxLayout()
        self.check_grp = QButtonGroup(check_layout)

        self.current_check = QCheckBox('Current Render Layer')
        self.all_check = QCheckBox('All Renderable Layers')

        check_layout.addWidget(self.current_check)
        check_layout.addWidget(self.all_check)

        self.check_grp.addButton(self.current_check)
        self.check_grp.addButton(self.all_check)

        separator_layout = QHBoxLayout()
        separator_layout.setContentsMargins(0, 0, 0, 0)
        separator_layout.setAlignment(Qt.AlignVCenter)
        frame = QFrame()
        frame.setFrameStyle(QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        separator_layout.addWidget(frame)

        cam_layout = QHBoxLayout()
        cam_label = QLabel('Render Camera')
        cam_label.setFixedWidth(80)
        self.cam_cb = QComboBox()
        cam_layout.addWidget(cam_label)
        cam_layout.addWidget(self.cam_cb)

        self.frame_te = QTextEdit()

        self.render_layout = QHBoxLayout()
        self.render_btn = QPushButton('Render')
        self.render_layout.addStretch()
        self.render_layout.addWidget(self.render_btn)

        main_layout.addLayout(check_layout)
        main_layout.addLayout(separator_layout)
        main_layout.addLayout(cam_layout)
        main_layout.addWidget(self.frame_te)
        main_layout.addLayout(self.render_layout)

        self.init_settings()
        self.set_signals()

    def init_settings(self):
        self.add_cam_option()

    def set_signals(self):
        self.render_btn.clicked.connect(self.do_render)

    def add_cam_option(self):
        cameras = self.utility.get_camera()
        self.cam_cb.addItems(cameras)
        self.cam_cb.setCurrentIndex(len(cameras) + 1)

    def do_render(self):
        if self.check_grp.checkedButton() == self.current_check:
            layers = self.utility.get_render_layer()
        else:
            layers = self.utility.get_render_layer("all")
        frames = str(self.frame_te.toPlainText())
        frames = get_range_data.get_range_data(frames)
        camera = self.cam_cb.currentText()
        if all((layers, camera, frames)):
            self.utility.render(layers, camera, frames)
        else:
            logging.warning("please select render layer & camera & frame")


def main():
    fr = FRenderView(get_maya_win.get_maya_win("PySide"))
    fr.show()


if __name__ == '__main__':
    main()
