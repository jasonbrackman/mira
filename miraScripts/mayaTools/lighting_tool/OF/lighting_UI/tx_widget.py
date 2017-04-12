# coding:utf-8
__author__ = 'heshuai'

from PySide import QtGui, QtCore
import maya.cmds as mc
import os
import public_ctrls
from get_parent_dir import get_parent_dir
import threading
import sys
import re


maketx_win = r'Z:/Resource/Support/aas_repos/aas_tools/mtoadeploy/1.2.3.1/2015/bin/maketx.exe'
maketx_linux = r'/mnt/v/Barajoun_Bilal_CG/software/development/productionTools/solidangle/mtoa/2014_1.1.2.2/bin/maketx'


def get_os_type():
    if sys.platform.startswith('win'):
        os_type = 'windows'
    elif sys.platform.startswith('linux'):
        os_type = 'linux'
    else:
        os_type = 'mac'
    return os_type


class TxWidget(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TxWidget, self).__init__(parent)
        # y_pos = public_ctrls.get_maya_main_win_pos()[1] + (public_ctrls.get_maya_main_win_size()[1])/4
        # self.move(public_ctrls.get_maya_main_win_pos()[0], y_pos)
        self.setWindowTitle('.tx textures')
        self.parent_dir = get_parent_dir()
        self.resize(500, 300)
        self.main_layout = QtGui.QVBoxLayout(self)
        label_layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel()
        self.label.setText('<font color="#00FF00" size=4><b>Textures</b> </font>')
        self.update_btn = QtGui.QToolButton()
        self.update_btn.setIcon(QtGui.QIcon(os.path.join(self.parent_dir, 'icons/button_icons/update.png')))
        self.update_btn.setStyleSheet('QToolButton{background: transparent}')
        label_layout.addWidget(self.label)
        label_layout.addWidget(self.update_btn)
        self.list_widget = QtGui.QListWidget()
        self.list_widget.setSelectionMode(QtGui.QListWidget.ExtendedSelection)
        self.list_widget.setSortingEnabled(True)
        self.list_widget.setSpacing(1)
        btn_layout = QtGui.QHBoxLayout()
        check_layout = QtGui.QHBoxLayout()
        self.check_grp = QtGui.QButtonGroup(check_layout)
        for i in ['To .tx', 'To jpg/tiff']:
            self.check_btn = QtGui.QCheckBox(i)
            self.check_btn.toggled.connect(self.switch_widget)
            check_layout.addWidget(self.check_btn)
            self.check_grp.addButton(self.check_btn)
        self.dis_select_all_btn = QtGui.QPushButton('Diselect All')
        self.dis_select_all_btn.setStyleSheet('QPushButton{color:#CCCCCC; background-color: #222222}')
        self.transform_btn = QtGui.QPushButton('Transform')
        self.transform_btn.setStyleSheet('QPushButton{color:#CCCCCC; background-color: #222222}')
        btn_layout.addLayout(check_layout)
        btn_layout.addStretch()
        btn_layout.addWidget(self.dis_select_all_btn)
        btn_layout.addWidget(self.transform_btn)
        self.main_layout.addLayout(label_layout)
        self.main_layout.addWidget(self.list_widget)
        self.main_layout.addLayout(btn_layout)
        self.set_background()
        self.set_signals()
        self.init_settings()

    def init_settings(self):
        for button in self.check_grp.buttons():
            if str(button.text()) == 'To .tx':
                button.setChecked(True)

    def init_tx_widget(self):
        self.list_widget.clear()
        all_files = mc.ls(type='file')
        all_textures = [mc.getAttr('%s.fileTextureName' % i) for i in all_files]
        all_textures = list(set(all_textures))
        for file_texture_name in all_textures:
            #if os.path.splitext(file_texture_name)[-1] != '.tx':
            tx_file_texture = os.path.splitext(file_texture_name)[0] + '.tx'
            if not os.path.isfile(tx_file_texture):
                item = QtGui.QListWidgetItem(file_texture_name)
                item.setIcon(QtGui.QIcon(os.path.join(self.parent_dir, 'icons', 'button_icons', 'textureItem.png')))
                self.list_widget.addItem(item)

    def init_other_widget(self):
        self.list_widget.clear()
        all_files = mc.ls(type='file')
        all_textures = [mc.getAttr('%s.fileTextureName' % i) for i in all_files]
        all_textures = list(set(all_textures))
        for file_texture_name in all_textures:
            if os.path.splitext(file_texture_name)[-1] == '.tx':
                item = QtGui.QListWidgetItem(file_texture_name)
                item.setIcon(QtGui.QIcon(os.path.join(self.parent_dir, 'icons', 'button_icons', 'textureItem.png')))
                self.list_widget.addItem(item)

    def switch_widget(self):
        if self.sender().text() == 'To .tx':
            self.label.setText('<font color="#00FF00" size=4><b>These textures are not .tx</b> </font>')
            self.init_tx_widget()
        else:
            self.label.setText('<font color="#00FF00" size=4><b>All .tx </b> </font>')
            self.init_other_widget()

    def set_background(self):
        image_path = os.path.join(self.parent_dir, 'icons', 'background_icons', 'tx.png')
        self.image = QtGui.QImage(image_path)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(self.image.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(self.image.scaled(event.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)))
        self.setPalette(palette)

    def set_signals(self):
        self.list_widget.itemSelectionChanged.connect(self.set_select)
        self.dis_select_all_btn.clicked.connect(self.dis_select_all)
        self.update_btn.clicked.connect(self.update)
        self.transform_btn.clicked.connect(self.transform)

    def set_select(self):
        for item in self.list_widget.selectedItems():
            for i in mc.ls(type='file'):
                if mc.getAttr('%s.fileTextureName' % i) == item.text():
                    mc.select(i, add=1)
                    break

    def select_all(self):
        for i in xrange(self.list_widget.count()):
            self.list_widget.item(i).setSelected(True)

    def dis_select_all(self):
        for i in xrange(self.list_widget.count()):
            self.list_widget.item(i).setSelected(False)

    def translate_texture(self, texture):
        if '$TANK' in texture:
            if get_os_type() == 'linux':
                texture = texture.replace('$TANK', '/mnt/tankprojects')
            if get_os_type() == 'windows':
                texture = texture.replace('$TANK', 'I:')
        if '$storage5' in texture:
            if get_os_type() == 'windows':
                texture = texture.replace('$storage5', 'K:/projectFiles')
        match_textures = []
        if '<udim>' in texture:
            pattern = os.path.basename(texture).replace('<udim>', '(\d{4})')
            texture_dir = os.path.dirname(texture)
            for i in os.listdir(texture_dir):
                if re.match(pattern, i):
                    match_textures.append(os.path.join(texture_dir, i))
        if match_textures:
            return match_textures
        else:
            return [texture]

    def transform_texture(self, texture_list):
        for texture in texture_list:
            if os.path.isfile(texture):
                if get_os_type() == 'windows':
                    os.system("%s -v --oiio \"%s\"" % (maketx_win, texture))
                if get_os_type() == 'linux':
                    os.system("%s -v --oiio %s" % (maketx_linux, texture))
                print "[OF] info:%s has been transformed" % texture
            else:
                print "[OF] error:%s is not an exist file" % texture

    def get_all_textures(self):
        all_textures = []
        exist_textures = []
        for item in self.list_widget.selectedItems():
            all_textures.extend(self.translate_texture(str(item.text())))
        if all_textures:
            for texture in all_textures:
                tx_texture = os.path.splitext(texture)[0] + '.tx'
                if os.path.isfile(tx_texture):
                    exist_textures.append(texture)
        return list(set(all_textures)-set(exist_textures))

    def re_group(self, file_list, n):
        if not isinstance(file_list, list) or not isinstance(n, int):
            return False
        elif n <= 0 or len(file_list) == 0:
            return False
        elif n >= len(file_list):
            return [[i] for i in file_list]
        elif n < len(file_list):
            new_list = []
            for x in xrange(n):
                new_list.append(list())
            while file_list:
                for x in xrange(n):
                    if file_list:
                        new_list[x].append(file_list.pop())
            for i in new_list:
                i.sort()
            return new_list

    def transform_to_tx(self):
        threads = []
        all_textures = self.get_all_textures()
        import pprint
        pprint.pprint(all_textures)
        if all_textures:
            group_textures = self.re_group(all_textures, 8)
            for texture_list in group_textures:
                t = threading.Thread(target=self.transform_texture, args=(texture_list, ))
                threads.append(t)
        if threads:
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        self.replace_tx()
        self.update()

    def replace_tx(self):
        selected_file_nodes = [i[0] for i in self.get_select_list()]
        for file_node in selected_file_nodes:
            file_texture_name = mc.getAttr('%s.fileTextureName' % file_node)
            if os.path.splitext(file_texture_name)[-1] != '.tx':
                new_texture_name = os.path.splitext(file_texture_name)[0]+'.tx'
                if '$TANK' in new_texture_name:
                    if get_os_type() == 'linux':
                        new_texture_name = new_texture_name.replace('$TANK', '/mnt/tankprojects')
                    if get_os_type() == 'windows':
                        new_texture_name = new_texture_name.replace('$TANK', 'I:')
                if '$storage5' in new_texture_name:
                    if get_os_type() == 'windows':
                        new_texture_name = new_texture_name.replace('$storage5', 'K:/projectFiles')
                if '<udim>' in new_texture_name:
                    pattern = os.path.basename(new_texture_name).replace('<udim>', '(\d{4})')
                    texture_dir = os.path.dirname(new_texture_name)
                    for i in os.listdir(texture_dir):
                        if re.match(pattern, i):
                            mc.setAttr(file_node+'.fileTextureName', new_texture_name, type='string')
                            print "[OF] info:%s has been replaced" % file_texture_name
                            break
                elif os.path.isfile(new_texture_name):
                    mc.setAttr(file_node+'.fileTextureName', new_texture_name, type='string')
                    print "[OF] info:%s has been replaced" % file_texture_name

    def get_select_list(self):
        ########get the list [node, node.fileTextureName]
        my_list = []
        for i in mc.ls(type='file'):
            for item in self.list_widget.selectedItems():
                if mc.getAttr('%s.fileTextureName' % i) == item.text():
                    my_list.append([i, str(item.text())])
        return my_list

    def transform_to_other(self):
        new_list = []
        if self.get_select_list():
            for arg in self.get_select_list():
                pattern = os.path.splitext(arg[1])[0] + '((.jpg)|(.tiff)|(.tif))$'
                new_list.append([arg[0], pattern])
        if new_list:
            for member in new_list:
                pattern = member[1].replace('\\', '/')
                if '$TANK' in member[1]:
                    if get_os_type() == 'linux':
                        pattern = member[1].replace('$TANK', '/mnt/tankprojects')
                    if get_os_type() == 'windows':
                        pattern = member[1].replace('$TANK', 'I:')
                if '$storage5' in member[1]:
                    if get_os_type() == 'windows':
                        pattern = member[1].replace('$storage5', 'K:/projectFiles')
                texture_dir = os.path.dirname(pattern)
                if os.path.isdir(texture_dir):
                    mark = 0
                    if '<udim>' not in pattern:
                        for i in os.listdir(texture_dir):
                            texture_name = os.path.join(texture_dir, i).replace('\\', '/')
                            if re.match(pattern, texture_name):
                                full_name = re.match(pattern, texture_name).group()
                                if os.path.isfile(full_name):
                                    mc.setAttr(member[0]+'.fileTextureName', full_name, type='string')
                                    print '[OF] info: replaced to %s' % full_name
                                    mark = 1
                                    break
                    else:
                        pattern = pattern.replace('<udim>', '(\d{4})')
                        for i in os.listdir(texture_dir):
                            texture_name = os.path.join(texture_dir, i).replace('\\', '/')
                            if re.match(pattern, texture_name):
                                full_name = re.match(pattern, texture_name).group()
                                mc.setAttr(member[0]+'.fileTextureName', re.sub('\d{4}', '<udim>', full_name), type='string')
                                print '[OF] info: replaced to %s' % mc.getAttr(member[0]+'.fileTextureName')
                                mark = 1
                    if mark == 0:
                        print '%s does not exist' % pattern
                else:
                    print '[OF] info: %s is not an exist dir' % texture_dir
        self.update()

    def transform(self):
        if self.check_grp.checkedButton().text() == 'To .tx':
            self.transform_to_tx()
        else:
            self.transform_to_other()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.close()

    def update(self):
        if self.check_grp.checkedButton().text() == 'To .tx':
            self.init_tx_widget()
        else:
            self.init_other_widget()


def run():
    global tx_widget
    try:
        tx_widget.close()
        tx_widget.deleteLater()
    except:pass
    tx_widget = TxWidget(public_ctrls.get_maya_win())
    tx_widget.show()