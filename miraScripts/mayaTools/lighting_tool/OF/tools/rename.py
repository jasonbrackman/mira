import os
import re
from PySide import QtGui, QtCore
import maya.cmds as mc


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
    
    
def get_maya_win():
    import maya.OpenMayaUI as mui
    main_window = None
    ptr = mui.MQtUtil.mainWindow()
    if 'PyQt4' in QtGui.__name__:
        import sip
        main_window = sip.wrapinstance(long(ptr), QtCore.QObject)
    if 'PySide' in QtGui.__name__:
        import shiboken
        main_window = shiboken.wrapInstance(long(ptr), QtCore.QObject)
    return main_window
    

class Rename(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Rename, self).__init__(parent)
        self.resize(500, 550)
        self.setObjectName('Rename')
        self.setWindowTitle('Rename')
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint)
        
        self.path = None
        
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(5, 10, 5, 5)
        layout_grp = QtGui.QGroupBox('System')
        layout_grp.setStyleSheet("QGroupBox{color:#00FF00;border: 1px solid #222222;"
                                          "padding-top:15px;border-radius:2px;font-size: 15px}")
        layout.addWidget(layout_grp)
        main_layout = QtGui.QVBoxLayout(layout_grp)
        file_layout = QtGui.QHBoxLayout()
        file_label = QtGui.QLabel('File Path')
        self.file_le = QtGui.QLineEdit()
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_le)
        
        self.lw = QtGui.QListWidget()
        self.lw.setSortingEnabled(True)
        self.lw.setSelectionMode(QtGui.QListWidget.ExtendedSelection)

        bottom_layout = QtGui.QHBoxLayout()
        
        rename_layout = QtGui.QGridLayout()
        src_label = QtGui.QLabel('Source Name')
        src_label.setAlignment(QtCore.Qt.AlignRight)
        self.src_le = QtGui.QLineEdit()
        
        dst_label = QtGui.QLabel('Destination Name')
        dst_label.setAlignment(QtCore.Qt.AlignRight)
        self.dst_le = QtGui.QLineEdit()
        
        rename_layout.addWidget(src_label, 0, 0)
        rename_layout.addWidget(self.src_le, 0, 1)
        rename_layout.addWidget(dst_label, 1, 0)
        rename_layout.addWidget(self.dst_le, 1, 1)
        
        rename_btn_layout = QtGui.QHBoxLayout()
        rename_btn_layout.setAlignment(QtCore.Qt.AlignTop)
        self.rename_btn = QtGui.QPushButton('Rename')
        self.rename_btn.setFixedHeight(50)
        rename_btn_layout.addWidget(self.rename_btn)
        
        bottom_layout.addLayout(rename_layout)
        bottom_layout.addLayout(rename_btn_layout)
        
        add_grp = QtGui.QGroupBox('Maya')
        add_grp.setStyleSheet("QGroupBox{color:#00FF00;border: 1px solid #222222;"
                                          "padding-top:15px;border-radius:2px;font-size: 15px}")
        add_layout = QtGui.QHBoxLayout(add_grp)
        
        maya_rename_layout = QtGui.QGridLayout()
        maya_src_label = QtGui.QLabel('Source Name')
        maya_src_label.setAlignment(QtCore.Qt.AlignRight)
        self.maya_src_le = QtGui.QLineEdit()
        maya_dst_label = QtGui.QLabel('Destination Name')
        maya_dst_label.setAlignment(QtCore.Qt.AlignRight)
        self.maya_dst_le = QtGui.QLineEdit()
        maya_rename_layout.addWidget(maya_src_label, 0, 0)
        maya_rename_layout.addWidget(self.maya_src_le, 0, 1)
        maya_rename_layout.addWidget(maya_dst_label, 1, 0)
        maya_rename_layout.addWidget(self.maya_dst_le, 1, 1)
        add_layout.addLayout(maya_rename_layout)
        
        self.maya_rename_btn = QtGui.QPushButton('Rename')
        self.maya_rename_btn.setFixedHeight(50)
        add_layout.addWidget(self.maya_rename_btn)
        
        
        main_layout.addLayout(file_layout)
        main_layout.addWidget(self.lw)
        main_layout.addLayout(bottom_layout)
        layout.addWidget(add_grp)
        
        self.set_signals()
        
    def set_signals(self):
        self.file_le.editingFinished.connect(self.set_item)
        self.rename_btn.clicked.connect(self.do_rename)
        self.maya_rename_btn.clicked.connect(self.maya_rename)
        
    def set_item(self):
        self.path = self.file_le.text()
        if os.path.isdir(self.path):
            self.lw.clear()
            for file in os.listdir(self.path):
                file_name = file.replace('\\', '/')
                item = QtGui.QListWidgetItem(file_name)
                self.lw.addItem(item)
                
    def do_rename(self):
        if self.lw.selectedItems():
            file_names = [item.text() for item in self.lw.selectedItems()]
            src_name = self.src_le.text()
            dst_name = self.dst_le.text()
            if all((src_name, dst_name)):
                for file_name in file_names:
                    old_file_name = os.path.join(self.path, file_name)
                    old_file_name = old_file_name.replace('\\', '/')
                    new_file_basename = re.sub(src_name, dst_name, file_name)
                    new_file_name = os.path.join(self.path, new_file_basename)
                    new_file_name = new_file_name.replace('\\', '/')
                    os.rename(old_file_name, new_file_name)
                    print "%s >> %s" % (old_file_name, new_file_name)
                self.set_item()
    
    @undo
    def maya_rename(self, *args):
        maya_src_name = self.maya_src_le.text()
        maya_dst_name = self.maya_dst_le.text()
        if all((maya_src_name, maya_dst_name)):
            for file in mc.ls(type='file'):
                texture_name = mc.getAttr('%s.fileTextureName' % file)
                if maya_src_name in texture_name:
                    prifix_name, file_name = os.path.split(texture_name)
                    new_file_name = re.sub(maya_src_name, maya_dst_name, file_name)
                    new_texture_name = os.path.join(prifix_name, new_file_name)
                    new_texture_name = new_texture_name.replace('\\', '/')
                    if os.path.isfile(new_texture_name):
                        mc.setAttr('%s.fileTextureName' % file, new_texture_name, type='string')

    @classmethod
    def show_ui(cls):
        if mc.window('Rename', q=1, exists=1):
            mc.deleteUI('Rename')
        atm = cls(get_maya_win())
        atm.show()
        

def main():
    Rename.show_ui()
    
    
if __name__ == '__main__':
    main()