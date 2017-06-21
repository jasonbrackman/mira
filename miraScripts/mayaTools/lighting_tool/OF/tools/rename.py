import os
import re
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from Qt import __binding__
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
    
    
def get_maya_win(module="PySide"):
    """
    get a QMainWindow Object of maya main window
    :param module (optional): string "PySide"(default) or "PyQt4"
    :return main_window: QWidget or QMainWindow object
    """
    import maya.OpenMayaUI as mui
    prt = mui.MQtUtil.mainWindow()
    if module == "PyQt":
        import sip
        from Qt.QtCore import *
        main_window = sip.wrapinstance(long(prt), QObject)
    elif module in ["PySide", "PyQt"]:
        if __binding__ in ["PySide", "PyQt4"]:
            import shiboken
        elif __binding__ in ["PySide2", "PyQt5"]:
            import shiboken2 as shiboken
        from Qt.QtWidgets import *
        main_window = shiboken.wrapInstance(long(prt), QWidget)
    elif module == "mayaUI":
        main_window = "MayaWindow"
    else:
        raise ValueError('param "module" must be "mayaUI" "PyQt4" or "PySide"')
    return main_window
    

class Rename(QDialog):
    def __init__(self, parent=None):
        super(Rename, self).__init__(parent)
        self.resize(500, 550)
        self.setObjectName('Rename')
        self.setWindowTitle('Rename')
        self.setWindowFlags(Qt.Dialog | Qt.WindowMinimizeButtonHint)
        
        self.path = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 10, 5, 5)
        layout_grp = QGroupBox('System')
        layout_grp.setStyleSheet("QGroupBox{color:#00FF00;border: 1px solid #222222;"
                                          "padding-top:15px;border-radius:2px;font-size: 15px}")
        layout.addWidget(layout_grp)
        main_layout = QVBoxLayout(layout_grp)
        file_layout = QHBoxLayout()
        file_label = QLabel('File Path')
        self.file_le = QLineEdit()
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_le)
        
        self.lw = QListWidget()
        self.lw.setSortingEnabled(True)
        self.lw.setSelectionMode(QListWidget.ExtendedSelection)

        bottom_layout = QHBoxLayout()
        
        rename_layout = QGridLayout()
        src_label = QLabel('Source Name')
        src_label.setAlignment(Qt.AlignRight)
        self.src_le = QLineEdit()
        
        dst_label = QLabel('Destination Name')
        dst_label.setAlignment(Qt.AlignRight)
        self.dst_le = QLineEdit()
        
        rename_layout.addWidget(src_label, 0, 0)
        rename_layout.addWidget(self.src_le, 0, 1)
        rename_layout.addWidget(dst_label, 1, 0)
        rename_layout.addWidget(self.dst_le, 1, 1)
        
        rename_btn_layout = QHBoxLayout()
        rename_btn_layout.setAlignment(Qt.AlignTop)
        self.rename_btn = QPushButton('Rename')
        self.rename_btn.setFixedHeight(50)
        rename_btn_layout.addWidget(self.rename_btn)
        
        bottom_layout.addLayout(rename_layout)
        bottom_layout.addLayout(rename_btn_layout)
        
        add_grp = QGroupBox('Maya')
        add_grp.setStyleSheet("QGroupBox{color:#00FF00;border: 1px solid #222222;"
                                          "padding-top:15px;border-radius:2px;font-size: 15px}")
        add_layout = QHBoxLayout(add_grp)
        
        maya_rename_layout = QGridLayout()
        maya_src_label = QLabel('Source Name')
        maya_src_label.setAlignment(Qt.AlignRight)
        self.maya_src_le = QLineEdit()
        maya_dst_label = QLabel('Destination Name')
        maya_dst_label.setAlignment(Qt.AlignRight)
        self.maya_dst_le = QLineEdit()
        maya_rename_layout.addWidget(maya_src_label, 0, 0)
        maya_rename_layout.addWidget(self.maya_src_le, 0, 1)
        maya_rename_layout.addWidget(maya_dst_label, 1, 0)
        maya_rename_layout.addWidget(self.maya_dst_le, 1, 1)
        add_layout.addLayout(maya_rename_layout)
        
        self.maya_rename_btn = QPushButton('Rename')
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
                item = QListWidgetItem(file_name)
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