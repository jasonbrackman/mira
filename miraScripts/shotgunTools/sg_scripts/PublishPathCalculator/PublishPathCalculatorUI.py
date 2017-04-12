#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/11/9'
# version     :
# usage       :
# notes       :

from PySide import QtGui
from PySide import QtCore
#import win32clipboard
#import win32con  
from PublishPathCalculator import PublishPathCalculator

class PublishPathcalculatorUI(QtGui.QDialog):

    def __init__(self, parent=None):
        super(PublishPathcalculatorUI, self).__init__(parent)

        self.path_calculator = PublishPathCalculator()

        self.setWindowTitle("Publish Path calculateor")
        self.main_layout = QtGui.QVBoxLayout(self)
        
        self.up_layout = QtGui.QHBoxLayout(self)
        self.main_layout.addLayout(self.up_layout)
        # 创建输入框
        self.asset_name_line = QtGui.QLineEdit()
        self.asset_name_line.setPlaceholderText("Type asset name here...")
        self.up_layout.addWidget(self.asset_name_line)
        # 创建task type combo
        self.task_type_combo = QtGui.QComboBox()
        self.task_type_combo.addItems(["mdl","art","rig"])
        self.up_layout.addWidget(self.task_type_combo)
        # 创建结果框
        self.result_line = QtGui.QLineEdit()
        self.result_line.setPlaceholderText("Result will be shown here...")
        #self.result_line.setEnabled(False)
        self.main_layout.addWidget(self.result_line)
        # 创建按钮
        self.calculate_button = QtGui.QPushButton()
        self.calculate_button.setText("calculate and Copy")
        self.main_layout.addWidget(self.calculate_button)
        
        # 连接按钮功能
        self.calculate_button.clicked.connect(self.on_calculate_button_clicked)
        
        # 设置宽度
        self.resize(500,100)
    
    def on_calculate_button_clicked(self):
        asset_name = self.asset_name_line.text()      
        task_type = self.task_type_combo.currentText()
        self.path_calculator = PublishPathCalculator()
        result = self.path_calculator.calculat(asset_name, task_type)
        self.result_line.setText(result)
        #self._write_in_clipboard(result)
    '''    
    def _write_in_clipboard(self, result):
        win32clipboard.OpenClipboard()  
        win32clipboard.EmptyClipboard()  
        win32clipboard.SetClipboardData(win32con.CF_TEXT, result)  
        win32clipboard.CloseClipboard()
    '''
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    ui = PublishPathcalculatorUI()
    ui.show()
    sys.exit(app.exec_())