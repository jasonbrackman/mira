import maya.cmds as mc
import pymel.core as pm
from PySide import QtGui, QtCore
import public_ctrls
from get_parent_dir import get_parent_dir
import os


def get_phong_list():
    return mc.ls(type='phong')


def undo(func):
    def _undo(*args, **kwargs):
        try:
            mc.undoInfo(ock=1)
            result = func(*args, **kwargs)
        except Exception, e:
            raise e
        else:
            return result
        finally:
            mc.undoInfo(cck=1)
    return _undo


ATTR_DICT = {'color': 'color',
             'incandescence': 'emissionColor',
             'normalCamera': 'normalCamera',
             'specularColor': 'KsColor',
             'transparency': 'opacity'}


class MayaUtility(object):

    def delete_file_node(self):
        for f in mc.ls(type='file'):
            if not mc.getAttr('%s.fileTextureName' % f):
                mc.delete(f)
        print "[OF] info: Delete null file node"

    def create_ar_shader(self):
        shader = mc.shadingNode('aiStandard', asShader=1)
        return shader

    def get_phong_shader(self):
        return mc.ls(type='phong')

    def get_sg_node(self, shader):
        sg_nodes = mc.listConnections('%s.outColor' % shader, s=0, d=1)
        return sg_nodes

    @undo
    def main(self):
        for phong_shader in self.get_phong_shader():
            sg_nodes = self.get_sg_node(phong_shader)
            if sg_nodes:
                ar_shader = self.create_ar_shader()
                for attr in ATTR_DICT:
                    source_attr = mc.listConnections('%s.%s' % (phong_shader, attr), s=1, d=0, plugs=1)
                    ar_attr = ATTR_DICT[attr]
                    if source_attr:
                        mc.connectAttr(source_attr[0], '%s.%s' % (ar_shader, ar_attr), f=1)
                    else:
                        value = mc.getAttr('%s.%s' % (phong_shader, attr))[0]
                        if attr == 'transparency':
                            mc.setAttr('%s.%s' % (ar_shader, ar_attr), 1-value[0], 1-value[1], 1-value[2], type='double3')
                        else:
                            mc.setAttr('%s.%s' % (ar_shader, ar_attr), value[0], value[1], value[2], type='double3')
                for sg_node in sg_nodes:
                    mc.connectAttr('%s.outColor' % ar_shader, '%s.surfaceShader' % sg_node, f=1)
                mc.delete(phong_shader)
                if 'phong' in phong_shader:
                    phong_shader = phong_shader.replace('phong', 'aiStandard')
                try:
                    mc.rename(ar_shader, phong_shader)
                except:pass


class CheckPhong(QtGui.QDialog):
    utility = MayaUtility()

    def __init__(self, parent=None):
        super(CheckPhong, self).__init__(parent)
        self.setWindowTitle('Check Phong')
        self.resize(400, 300)
        self.parent_dir = get_parent_dir()
        self.image = None
        self.setStyleSheet("QDialog{background-color: transparent}")
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(1, 1, 1, 1)
        frame = QtGui.QFrame()
        main_layout.addWidget(frame)
        frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout_of_frame = QtGui.QVBoxLayout(frame)
        layout_of_frame.setContentsMargins(1, 1, 1, 1)
        layout_of_frame.setSpacing(5)
        #---------------------------------label layout------------------------------------------------#
        label_layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel()
        self.label.setText('<font size=4 color="#00FF00"><b>Phong Materials</b></font>')
        self.label.setStyleSheet("QLabel{background-color: transparent}")
        self.update_btn = QtGui.QToolButton()
        self.update_btn.setIcon(QtGui.QIcon(os.path.join(self.parent_dir, 'icons', 'button_icons', 'update.png')))
        self.update_btn.setStyleSheet("QToolButton{background-color: transparent}")
        label_layout.addWidget(self.label)
        label_layout.addWidget(self.update_btn)
        #---------------------------------separate layout-----------------------------------------------#
        separate_layout = QtGui.QHBoxLayout()
        separate_layout.setContentsMargins(0, 0, 0, 0)
        separate_frame = QtGui.QFrame()
        separate_frame.setStyleSheet('QFrame{color: #118811}')
        separate_frame.setFrameStyle(QtGui.QFrame.HLine)
        separate_layout.addWidget(separate_frame)
        #---------------------------------list widget------------------------------------------------#
        self.phong_list = QtGui.QListWidget()
        self.phong_list.setStyleSheet("QListWidget{background-color: transparent}")
        self.phong_list.setSelectionMode(QtGui.QListWidget.ExtendedSelection)
        self.phong_list.setSortingEnabled(True)
        #---------------------------------Convert    ------------------------------------------------#
        self.convert_btn = QtGui.QPushButton('Convert All Phong Shader To aiStandard')
        self.convert_btn.setStyleSheet("QPushButton{color: #00FF00; background-color: #112211}")
        #---------------------------------------------------------------------------------------------#
        layout_of_frame.addLayout(label_layout)
        layout_of_frame.addLayout(separate_layout)
        layout_of_frame.addWidget(self.phong_list)
        layout_of_frame.addWidget(self.convert_btn)

        self.set_background()
        self.init_settings()
        self.set_signals()

    def set_background(self):
        image_path = os.path.join(self.parent_dir, 'icons/background_icons/phong.png')
        self.image = QtGui.QImage(image_path)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(self.image.scaled(self.size(),
                         QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(self.image.scaled(event.size(),
                         QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)

    def set_signals(self):
        self.update_btn.clicked.connect(self.do_update)
        self.phong_list.itemSelectionChanged.connect(self.set_select)
        self.convert_btn.clicked.connect(self.do_convert)

    def init_settings(self):
        phong_list = get_phong_list()
        if phong_list:
            for phong in phong_list:
                item = PhongItem(phong)
                self.phong_list.addItem(item)
        else:
            self.close()
            QtGui.QMessageBox.information(None, "Information", "No Phong")

    def do_update(self):
        self.phong_list.clear()
        self.init_settings()

    def set_select(self):
        selected_items = self.phong_list.selectedItems()
        selected_phongs = [str(item.text()) for item in selected_items]
        pm.select(selected_phongs, r=1)

    def do_convert(self):
        self.utility.main()
        self.do_update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.close()

    @classmethod
    def main(cls):
        global cp
        try:
            cp.close()
            cp.deleteLater()
        except:pass
        cp = cls(public_ctrls.get_maya_win())
        cp.show()


class PhongItem(QtGui.QListWidgetItem):
    def __init__(self, text=None, parent=None):
        super(PhongItem, self).__init__(parent)
        self.setText(text)
        self.parent_dir = get_parent_dir()
        icon_path = os.path.join(self.parent_dir, 'icons/button_icons', 'phong.png')
        self.setIcon(QtGui.QIcon(icon_path))


def run():
    if not get_phong_list():
        QtGui.QMessageBox.information(None, "Information", "No Phong")
    else:
        CheckPhong.main()


if __name__ == '__main__':
    run()