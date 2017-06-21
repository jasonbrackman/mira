__author__ = 'heshuai'

from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import os
import functools
import xml.dom.minidom
# local modules
import add_environ
import maya_ctrls
reload(maya_ctrls)
import public_ctrls
reload(public_ctrls)
from get_parent_dir import get_parent_dir


class MainUI(QMainWindow):

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setWindowTitle('Lighting Tools')
        self.setWindowOpacity(0.7)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.SplashScreen)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(645, 40)
        self.parent_dir = get_parent_dir()
        self.UI_status = 1
        self.set_background()
        # create action
        self.setup_ui()
        # tool bar
        self.follow_maya_win()
        try:
            maya_ctrls.set_persp_far()
        except:
            pass

    def set_background(self):
        image_path = os.path.join(
            self.parent_dir, 'icons', 'background_icons', 'main.png')
        self.image = QImage(image_path)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.image.scaled(
            self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.image.scaled(
            event.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def get_conf_xml_path(self):
        conf_xml_path = os.path.join(self.parent_dir, 'config', 'lighting_tool_actions.xml')
        conf_xml_path = conf_xml_path.replace('\\', '/')
        return conf_xml_path

    def setup_ui(self):
        conf_xml_path = self.get_conf_xml_path()
        dom_tree = xml.dom.minidom.parse(conf_xml_path)
        collection = dom_tree.documentElement
        toolbars = collection.getElementsByTagName('toolbar')
        for toolbar in toolbars:
            lighting_toolbar = self.addToolBar(collection.getAttribute('name'))
            lighting_toolbar.setMovable(False)
            actions = toolbar.getElementsByTagName('action')
            for action in actions:
                action_type = action.getAttribute('type')
                if action_type == 'command':
                    action_name = action.getAttribute('name')
                    command = action.getAttribute('command')
                    lighting_action = Action(action_name, self)
                    lighting_action.triggered.connect(functools.partial(self.exec_command, command))
                    lighting_toolbar.addAction(lighting_action)
            self.addToolBarBreak()

    def exec_command(self, command):
        exec(command)

    def convert_tex_path(self):
        mel_path = os.path.join(
            self.parent_dir, 'maya_ctrls', 'FileTextureManager.mel')
        mel_path = mel_path.replace('\\', '/')
        print mel_path
        import maya.mel as mel
        mel.eval("source \"%s\";" % mel_path)
        mel.eval("FileTextureManager;")

    def do_close(self):
        self.close()

    def do_help(self):
        from maya_ctrls import get_os_type
        os_type = get_os_type.get_os_type()
        if os_type == 'windows':
            os.startfile(os.path.join(self.parent_dir, 'help.docx'))
        if os_type == 'linux':
            os.system('xdg-open %s' % os.path.join(
                self.parent_dir, 'help.docx'))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPositon = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPositon)
            event.accept()

    def enterEvent(self, event):
        self.setWindowOpacity(1)

    def leaveEvent(self, event):
        self.setWindowOpacity(0.7)

    '''
    def moveEvent(self, event):
        if [self.pos().x(), self.pos().y()] != public_ctrls.get_maya_main_win_pos():
            self.follow_maya_win()
    '''

    def follow_maya_win(self):
        add_stretch = public_ctrls.get_maya_main_win_size()[0]/4
        self.move(public_ctrls.get_maya_main_win_pos()[0]+add_stretch, public_ctrls.get_maya_main_win_pos()[1]+40)

    def switch_UI_status(self):
        self.UI_status = not self.UI_status
        if self.UI_status:
            maya_ctrls.show_UI_elements()
        else:
            maya_ctrls.hide_UI_elements()
        self.follow_maya_win()


class Action(QAction):

    def __init__(self, name=None, parent=None):
        super(Action, self).__init__(parent)
        parent_dir = get_parent_dir()
        icon_path = os.path.join(
            parent_dir, 'icons', 'main_icons', name+'.png')
        self.setIcon(QIcon(icon_path))
        self.setText(name)


def load_arnold():
    from maya_ctrls import load_plugin
    reload(load_plugin)
    try:
        load_plugin.load_plugin('mtoa.mll')
    except:
        print '[AAS] info: Arnold load failed'


def run():
    global lt
    try:
        lt.close()
        lt.deleteLater()
    except:
        pass
    lt = MainUI(public_ctrls.get_maya_win())
    lt.show()

if __name__ == '__main__':
    load_arnold()
    run()
