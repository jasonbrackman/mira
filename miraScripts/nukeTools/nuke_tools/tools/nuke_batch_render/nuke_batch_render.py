import subprocess
from PySide import QtGui, QtCore
import os
import threading


nuke_path = 'C:/Program Files/Nuke9.0v5/Nuke9.0.exe'
script_path = 'E:/nuke_tool/nuke_batch_render/nuke_render.py'


def get_line(nuke_path, nuke_script_path, nuke_file):
    command = "\"%s\" -t %s %s" % (nuke_path, nuke_script_path, nuke_file)
    #print command
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        ret_code = p.poll()
        if ret_code == 0:
            break
        elif ret_code == 1:
            raise Exception('Nuke was terminated for some reason')
        elif ret_code is not None:
            raise Exception('Error:', ret_code)
        line = p.stdout.readline()
        yield line
        
        
#--------------------------------GetNukePathWidget-------------------------------#
class GetNukePathWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(GetNukePathWidget, self).__init__(parent)
        main_layout = QtGui.QHBoxLayout(self)
        label = QtGui.QLabel('Nuke Path')
        label.setFixedWidth(60)
        self.nuke_path_le = QtGui.QLineEdit()
        self.btn = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon))
        self.btn.setIcon(icon)
        
        main_layout.addWidget(label)
        main_layout.addWidget(self.nuke_path_le)
        main_layout.addWidget(self.btn)
        
        self.set_signals()
        
    def set_signals(self):
        self.btn.clicked.connect(self.get_nuke_path)
        
    def get_nuke_path(self):
        file_dialog = QtGui.QFileDialog()
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        file_path = file_dialog.getOpenFileName(self, 'choose nuke path', '/',
                                                "Nuke File(*.exe)")                                 
        self.nuke_path_le.setText(file_path[0])
        

#-----------------------------------file  widget-----------------------------------#
class AttrLayout(QtGui.QHBoxLayout):
    def __init__(self, parent=None):
        super(AttrLayout, self).__init__(parent)
        
        self.write_cb = QtGui.QCheckBox()
        self.write_cb.setChecked(True)
        self.frame_le = QtGui.QLineEdit()
        self.frame_le.setFixedWidth(80)
        self.dir_le = QtGui.QLineEdit() 
        
        self.addWidget(self.write_cb)
        self.addWidget(self.frame_le)
        self.addWidget(self.dir_le)
        
        
class NukeItem(QtGui.QListWidgetItem):
    def __init__(self, name=None, nuke_path=None, parent=None):
        super(NukeItem, self).__init__(parent)
        self.name = name
        self.setText(self.name)
        self.nuke_path = nuke_path
        self.widget = QtGui.QWidget(parent = MainWidget.attr_widget)
        self.layout = QtGui.QVBoxLayout(self.widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.info_browser = QtGui.QTextBrowser()
        self.init_settings()

    def init_settings(self):
        if self.get_attr():
            print self.get_attr()
            for attr in self.get_attr():
                attr_layout = AttrLayout()
                name, frame_range, render_dir = attr.split(',')
                if name:
                    attr_layout.write_cb.setText(name)
                if frame_range:
                    attr_layout.frame_le.setText(frame_range)
                if render_dir:
                    attr_layout.dir_le.setText(render_dir)
                self.layout.addLayout(attr_layout)
                
    def get_attr(self):
        my_nodes_attrs = list()
        for line in get_line(self.nuke_path, script_path, self.name):
            if line.startswith('My Write Node'):
                my_node_attr = line.split('@')[-1].strip()
                my_nodes_attrs.append(my_node_attr)
        return my_nodes_attrs
        
        
class FileListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent)
        self.nuke_path = nuke_path
        self.setSelectionMode(QtGui.QListWidget.ExtendedSelection)
        self.setSortingEnabled(True)
        self.setAcceptDrops(True)
        self.setSpacing(1)
        
    def add_item(self, path, nuke_path):
        exist_item = []
        if self.count():
            for x in xrange(self.count()):
                exist_item.append(str(self.item(x).text()))
        all_files = list()
        if os.path.isfile(path) and os.path.splitext(path)[-1]== '.nk':
                if exist_item:
                    if path.replace('\\', '/') not in exist_item:
                        all_files.append(path)
                else:
                    all_files.append(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    if os.path.splitext(f)[-1] == '.nk':
                        all_files.append(os.path.join(root, f))
                        all_files = [f.replace('\\', '/') for f in all_files]
            if all_files and exist_item:
                    all_files = list(set(all_files)-set(exist_item) & set(all_files))
        if all_files:
            for f in all_files:
                item = NukeItem(f, nuke_path)
                self.addItem(item)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        threads = list()
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            t = threading.Thread(target=self.add_item, args=(path, nuke_path))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            

class FileWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.lw = FileListWidget()
        main_layout.addWidget(self.lw)
        

#-----------------------------------attr  widget-----------------------------------#
class AttrWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AttrWidget, self).__init__(parent)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        
        scroll_area = QtGui.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        
        scroll_widget = QtGui.QWidget()
        scroll_area.setWidget(scroll_widget)
        
        self.scroll_widget_layout = QtGui.QVBoxLayout()
        self.widget = QtGui.QStackedWidget()
        self.scroll_widget_layout.addWidget(self.widget)
        
        button_layout = QtGui.QHBoxLayout()
        self.render_btn = QtGui.QPushButton('Render...')
        button_layout.addStretch()
        button_layout.addWidget(self.render_btn)
        
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(button_layout)
        

#-----------------------------------attr  widget-----------------------------------#
class InfoWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(InfoWidget, self).__init__(parent)
        self.main_layout = QtGui.QVBoxLayout(self)

        
#-----------------------------------main  widget-----------------------------------#
class MainWidget(QtGui.QDialog):
    nuke_path_widget = None
    file_list_widget = None
    attr_widget = None
    info_widget = None

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.nuke_path_widget = GetNukePathWidget()
        self.file_list_widget = FileWidget()
        self.attr_widget = AttrWidget()
        self.info_widget = InfoWidget()
        
        nuke_path_frame = FrameWidget()
        nuke_path_frame.main_layout.addWidget(self.nuke_path_widget)
        
        bottom_layout = QtGui.QVBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        main_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        bottom_layout.addWidget(main_splitter)
        file_list_frame = FrameWidget(main_splitter)
        file_list_frame.main_layout.addWidget(self.file_list_widget)
        
        right_splitter = QtGui.QSplitter(QtCore.Qt.Vertical, main_splitter)
        attr_frame = FrameWidget(right_splitter)
        attr_frame.main_layout.addWidget(self.attr_widget)
        
        info_frame = FrameWidget(right_splitter)
        info_frame.main_layout.addWidget(self.info_widget)

        main_layout.addWidget(nuke_path_frame)
        main_layout.addLayout(bottom_layout)
        
        self.set_signals()
        
    def set_signals(self):
        self.file_list_widget.lw.itemClicked.connect(self.show_attr)
        
    def show_attr(self, item):
        item.widget.setParent(self.attr_widget.widget)
        self.attr_widget.widget.addWidget(item.widget)
        self.attr_widget.widget.setCurrentWidget(item.widget)
        self.info_widget.main_layout.addWidget(item.info_browser)

#-----------------------------------frame  widget-----------------------------------#
class FrameWidget(QtGui.QFrame):
    def __init__(self, parent=None):
        super(FrameWidget, self).__init__(parent)
        self.main_layout = QtGui.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QtGui.QFrame.Panel|QtGui.QFrame.Raised)    
        

fw = MainWidget()
fw.show()