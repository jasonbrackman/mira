#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraLibs.mayaLibs import get_maya_win
import functools
import add_group_tool

reload(add_group_tool)


class Group(QDialog):
    def __init__(self, parent=None):
        super(Group, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle(self.tr('Group Kit'))
        self.setObjectName('group_kit')
        self.setMinimumSize(538, 570)
        self.setMaximumSize(538, 570)

        self.icon_dir = os.path.join(os.path.dirname(__file__), "icons")

        '''create layout'''
        main_layout = QVBoxLayout(self)

        character_layout = QVBoxLayout()
        # character_layout.setAlignment(Qt.AlignTop)
        prop_layout = QHBoxLayout()
        scene_layout = QHBoxLayout()

        # button_layout = QHBoxLayout()

        '''create palette'''
        frame_palette = QPalette()
        frame_palette.setColor(self.backgroundRole(), QColor(255, 0, 0))

        '''create widget'''
        tab_widget = QTabWidget()

        character_tab_frame = QFrame()
        character_tab_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        # character_tab_frame.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        character_tab_frame.setAutoFillBackground(True)

        frame_palette.setBrush(self.backgroundRole(),
                               QBrush(QPixmap(os.path.join(self.icon_dir, "man.png"))))
        character_tab_frame.setPalette(frame_palette)

        character_widget = QWidget()
        character_widget.setContentsMargins(0, 0, 0, 0)

        self.__grp_button_dict = {'body': (170, 170),
                                  'cloth_up': (160, 120),
                                  'cloth_down': (151, 220),
                                  'left_shoe': (102, 440),
                                  'right_shoe': (215, 440),
                                  'mouth': (385, 190),
                                  'gums': (390, 305),
                                  'up_gums': (380, 270),
                                  'down_gums': (370, 340),
                                  'eye': (393, 130),
                                  'left_eyeball': (330, 155),
                                  'right_eyeball': (415, 155),
                                  'left_eyeball_inside': (270, 100),
                                  'right_eyeball_inside': (380, 100),
                                  'other': (0, 480),
                                  }

        for key, value in self.__grp_button_dict.iteritems():
            character_pushbutton = QPushButton(key, character_widget)
            character_pushbutton.move(value[0], value[1])
            character_pushbutton.setMaximumWidth(character_pushbutton.sizeHint().width())
            character_pushbutton.setStyleSheet('QPushButton {background-color: rgba(0,0,0,0);}')
            character_pushbutton.clicked.connect(functools.partial(self.add_group, character_pushbutton))

        prop_tab_frame = QFrame()
        prop_tab_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        prop_tab_frame.setAutoFillBackground(True)

        frame_palette.setBrush(self.backgroundRole(),
                               QBrush(QPixmap(os.path.join(self.icon_dir, "prop.png"))))
        prop_tab_frame.setPalette(frame_palette)

        prop_widget = QWidget()
        prop_widget.setContentsMargins(0, 0, 0, 0)

        scene_tab_frame = QFrame()
        scene_tab_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        scene_tab_frame.setAutoFillBackground(True)

        frame_palette.setBrush(self.backgroundRole(),
                               QBrush(QPixmap(os.path.join(self.icon_dir, "scene.png"))))
        scene_tab_frame.setPalette(frame_palette)

        scene_widget = QWidget()
        scene_widget.setContentsMargins(0, 0, 0, 0)

        # add_button = QPushButton('Add to group')
        # add_button.clicked.connect(self.add_group)

        '''add widget'''
        # palette1.setColor(sss.backgroundRole(), QColor(192, 253, 123))
        # brush = QBrush(QColor(255,0,0))
        # brush.setTexture(icon)
        # brush.setStyle(Qt.TexturePattern)
        # palette1.setBrush(QPalette.Active, QPalette.Window, brush)
        # # sss.color = QColor(0, 0, 255)
        #
        # character_tab_frame.setLayout(character_layout)
        # character_layout.addWidget(sss)
        #
        # ba=QPushButton('ddddddddddddddddd')
        #
        # character_layout.addWidget(ba)

        tab_widget.addTab(character_tab_frame, 'Character')
        tab_widget.addTab(prop_tab_frame, 'Prop')
        tab_widget.addTab(scene_tab_frame, 'Scene')

        main_layout.addWidget(tab_widget)

        character_layout.addWidget(character_widget)
        prop_layout.addWidget(prop_widget)
        scene_layout.addWidget(scene_widget)

        # character_tab_frame.addWidget(body_radiobutton)
        # character_tab_frame.addWidget(cloth_up_radiobutton)

        # button_layout.addWidget(add_button)

        '''add layout'''
        # main_layout.addLayout(button_layout)
        character_tab_frame.setLayout(character_layout)

    def add_group(self, grp_name):
        except_list = [key+'_grp' for key in self.__grp_button_dict.keys()]
        add_group_tool.add_sel_to_group(grp_name.text()+'_grp', except_list)


def main():
    main_win = Group(get_maya_win.get_maya_win('PySide'))
    main_win.show()

if __name__ == '__main__':
    main()
