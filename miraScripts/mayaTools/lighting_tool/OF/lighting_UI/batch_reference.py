
from PySide import QtGui, QtCore
import maya.cmds as mc
import maya.OpenMayaUI as mui
import sip
import os


def get_maya_win():
    prt = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(prt), QtGui.QWidget)


def reference_file(maya_file):
    namespace = os.path.splitext(os.path.basename(maya_file))[0]
    mc.file(maya_file, r=1, namespace=namespace, shd=("displayLayers", "shadingNetworks"))
    

class BatchReference(QtGui.QDialog):
    def __init__(self, parent=None):
        super(BatchReference, self).__init__(parent)
        self.setWindowTitle('Batch Reference')
        self.resize(380, 350)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_frame = QtGui.QFrame()
        main_layout.addWidget(main_frame)
        main_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout_of_frame = QtGui.QVBoxLayout(main_frame)
        self.file_path = None
        #----------------------------file layout--------------------------------#
        file_layout = QtGui.QHBoxLayout()
        file_label = QtGui.QLabel('file Directory')
        file_label.setFixedWidth(65)
        file_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.file_le = QtGui.QLineEdit()
        self.file_btn = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon))
        self.file_btn.setIcon(icon)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_le)
        file_layout.addWidget(self.file_btn)
        #----------------------------list widget--------------------------------#
        self.lw = QtGui.QListWidget()
        self.lw.setSelectionMode(QtGui.QListWidget.ExtendedSelection)
        self.lw.setSortingEnabled(True)
        self.lw.setSpacing(1)
        #---------------------------separator layout-------------------------------#
        separator_layout = QtGui.QHBoxLayout()
        separator_layout.setContentsMargins(0, 10, 0, 0)
        separator_layout.setAlignment(QtCore.Qt.AlignBottom)
        frame = QtGui.QFrame()
        frame.setFrameStyle(QtGui.QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        separator_layout.addWidget(frame)
        #---------------------------separator layout-------------------------------#
        ref_layout = QtGui.QHBoxLayout()
        self.ref_btn = QtGui.QPushButton('Reference')
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
        file_dialog = QtGui.QFileDialog()
        file_dialog.setFileMode(QtGui.QFileDialog.Directory)
        self.file_path = file_dialog.getExistingDirectory(self, 'choose the image file', '/', QtGui.QFileDialog.DontUseSheet)
        self.file_le.setText(self.file_path)

    def add_item(self, dir):
        self.lw.clear()
        if os.path.isdir(dir):
            for file in os.listdir(dir):
                if os.path.isfile(os.path.join(dir, file)):
                    if os.path.splitext(file)[-1] in ['.ma', '.mb']:
                        item = QtGui.QListWidgetItem(file)
                        file_info = QtCore.QFileInfo(os.path.join(dir, file))
                        icon_provider = QtGui.QFileIconProvider()
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