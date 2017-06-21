
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import maya.OpenMayaUI as mui
import sip
import os


def get_maya_win():
    prt = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(prt), QWidget)


def reference_file(maya_file):
    namespace = os.path.splitext(os.path.basename(maya_file))[0]
    mc.file(maya_file, r=1, namespace=namespace, shd=("displayLayers", "shadingNetworks"))
    

class BatchReference(QDialog):
    def __init__(self, parent=None):
        super(BatchReference, self).__init__(parent)
        self.setWindowTitle('Batch Reference')
        self.resize(380, 350)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_frame = QFrame()
        main_layout.addWidget(main_frame)
        main_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        layout_of_frame = QVBoxLayout(main_frame)
        self.file_path = None
        #----------------------------file layout--------------------------------#
        file_layout = QHBoxLayout()
        file_label = QLabel('file Directory')
        file_label.setFixedWidth(65)
        file_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.file_le = QLineEdit()
        self.file_btn = QToolButton()
        icon = QIcon()
        icon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon))
        self.file_btn.setIcon(icon)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_le)
        file_layout.addWidget(self.file_btn)
        #----------------------------list widget--------------------------------#
        self.lw = QListWidget()
        self.lw.setSelectionMode(QListWidget.ExtendedSelection)
        self.lw.setSortingEnabled(True)
        self.lw.setSpacing(1)
        #---------------------------separator layout-------------------------------#
        separator_layout = QHBoxLayout()
        separator_layout.setContentsMargins(0, 10, 0, 0)
        separator_layout.setAlignment(Qt.AlignBottom)
        frame = QFrame()
        frame.setFrameStyle(QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        separator_layout.addWidget(frame)
        #---------------------------separator layout-------------------------------#
        ref_layout = QHBoxLayout()
        self.ref_btn = QPushButton('Reference')
        ref_layout.addStretch()
        ref_layout.addWidget(self.ref_btn)
        #----------------------------------------------------------------------------#
        layout_of_frame.addLayout(file_layout)
        layout_of_frame.addWidget(self.lw)
        layout_of_frame.addLayout(separator_layout)
        layout_of_frame.addLayout(ref_layout)
        #----------------------------------------------------------------------------#
        self.set_signals()

    def set_signals(self):
        self.file_le.textChanged.connect(self.add_item)
        self.file_btn.clicked.connect(self.get_file_dir)
        self.ref_btn.clicked.connect(self.do_reference)
        
    def get_file_dir(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        self.file_path = file_dialog.getExistingDirectory(self, 'choose the image file', '/', QFileDialog.DontUseSheet)
        self.file_le.setText(self.file_path)

    def add_item(self, dir):
        self.lw.clear()
        if os.path.isdir(dir):
            for file in os.listdir(dir):
                if os.path.isfile(os.path.join(dir, file)):
                    if os.path.splitext(file)[-1] in ['.ma', '.mb']:
                        item = QListWidgetItem(file)
                        file_info = QFileInfo(os.path.join(dir, file))
                        icon_provider = QFileIconProvider()
                        icon = icon_provider.icon(file_info)
                        item.setIcon(icon)
                        self.lw.addItem(item)

    def do_reference(self):
        if self.lw.selectedItems():
            ref_files = [os.path.join(str(self.file_le.text()), str(item.text())) for item in self.lw.selectedItems()]
            for file in ref_files:
                reference_file(file)


def main():
    global br
    try:
        br.close()
        br.deleteLater()
    except:pass
    br = BatchReference(get_maya_win())
    br.show()


if __name__ == '__main__':
    main()