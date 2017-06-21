#! /usr/bin/env python
#coding=utf-8
#File       : shave_color_correction.py
#Description: Correct Color of ShaveHair Node at "RenderView" Mode and "KICK-ASS" Mode
#Author     : heshuai, Yan-Chen Liao
#Modified   :
#Note       :
import pymel.core as pm
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as cmds
import public_ctrls

windowObject = 'ShaveHair Gamma Correction'


class ShaveGammaCorrection(QDialog):
    def __init__(self, parent=None):
        super(ShaveGammaCorrection, self).__init__(parent)
        y_pos = public_ctrls.get_maya_main_win_pos()[1] + (public_ctrls.get_maya_main_win_size()[1])/4
        self.move(public_ctrls.get_maya_main_win_pos()[0], y_pos)
        self.setObjectName(windowObject)
        self.setWindowTitle(windowObject)
        self.resize(300, 50)
        main_layout = QVBoxLayout(self)
        self.status_label = QLabel()
        self.correct_btn = QPushButton('Correct')
        self.recover_btn = QPushButton('Recover')
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.correct_btn)
        main_layout.addWidget(self.recover_btn)
        self.colAttrs =['specularTint', 'specularTint2',
                'hairColor', 'rootColor', 'mutantHairColor']
        self.init_settings()
        self.set_signals()

    def init_settings(self):
        node = pm.PyNode('persp')
        if hasattr(node, 'Gammainfo'):
            if int(node.Gammainfo.get()):
                self.set_status_recover()
            else:
                self.set_status_correct()
        else:
            self.add_attr()
            self.set_status_correct()

    def set_signals(self):
        self.correct_btn.clicked.connect(self.gamma_correct)
        self.recover_btn.clicked.connect(self.gamma_recover)

    def set_status_recover(self):
        self.status_label.setText('Status: <font size=4 color="#FF0000"><b>KICK-ASS Rendering Mode')
        self.correct_btn.setEnabled(False)
        self.recover_btn.setEnabled(True)
        pm.PyNode('persp').Gammainfo.set('1')

    def set_status_correct(self):
        self.status_label.setText('Status: <font size=4 color="#3da8b2"><b>RenderView Mode')
        self.recover_btn.setEnabled(False)
        self.correct_btn.setEnabled(True)
        pm.PyNode('persp').Gammainfo.set('0')

    def add_attr(self):
        if not hasattr(pm.PyNode('persp'), 'Gammainfo'):
            pm.select(clear=1)
            pm.select('persp')
            pm.addAttr(longName='Gammainfo', dataType='string')
            pm.PyNode('persp').Gammainfo.set('0')

    def gamma_correction(self, col, gamma):
        return (pow(col[0], gamma), pow(col[1], gamma), pow(col[2], gamma))

    # Correct Colors for Rendering on Render Farm
    def gamma_correct(self):
        for shave in pm.ls(type='shaveHair'):
            for attr in self.colAttrs:
                try:
                    attrNode = pm.PyNode('%s.%s' % (shave.name(), attr))
                    ocol = attrNode.get()
                    attrNode.set(self.gamma_correction(ocol, 2.2))
                except:pass
        self.add_attr()
        self.set_status_recover()

    # Restore Colors for Local Render View Rendering
    def gamma_recover(self):
        for shave in pm.ls(type='shaveHair'):
            for attr in self.colAttrs:
                try:
                    attrNode = pm.PyNode('%s.%s' % (shave.name(), attr))
                    ocol = attrNode.get()
                    attrNode.set(self.gamma_correction(ocol, 1.0/ 2.2))
                except:pass
        self.add_attr()
        self.set_status_correct()


def run():
    if cmds.window(windowObject, q=True, exists=True):
        cmds.deleteUI(windowObject)
    sgc = ShaveGammaCorrection(public_ctrls.get_maya_win())
    sgc.show()

if __name__ == '__main__':
    run()