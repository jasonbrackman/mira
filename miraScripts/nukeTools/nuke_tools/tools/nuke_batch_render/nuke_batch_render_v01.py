import subprocess
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import os
import threading
import re


nuke_path = 'C:/Program Files/Nuke9.0v5/Nuke9.0.exe'
script_path = 'E:/nuke_tool/nuke_batch_render/nuke_render.py'


def get_write_info(nuke_file):
    f = open(nuke_file, 'r')
    value = f.readlines()
    f.close()

    value = ''.join(value)

    pattern_write = r'Write\s*\{[^{}]*\}'
    pattern_viewer = r'Viewer\s*\{[^{}]*\}'

    pattern_name = 'name ([^\n]*)'
    pattern_file = 'file ([^\n]*)'
    pattern_frame_range = 'frame_range ([^\n]*)'

    viewer_nodes = re.findall(pattern_viewer, value)
    frame_range = re.findall(pattern_frame_range, viewer_nodes[0])[0]

    write_nodes = re.findall(pattern_write, value)

    write_node_information = list()
    if write_nodes:
        for node in write_nodes:
            temp = list()
            try:
                write_name = re.findall(pattern_name, node)[0]
            except:
                write_name = ''
            try:
                write_file = re.findall(pattern_file, node)[0]
            except:
                write_file = ''
            temp.append([write_name, frame_range, write_file])
            write_node_information.extend(temp)

    return write_node_information

        
#--------------------------------GetNukePathWidget-------------------------------#
class GetNukePathWidget(QWidget):
    def __init__(self, parent=None):
        super(GetNukePathWidget, self).__init__(parent)
        main_layout = QHBoxLayout(self)
        self.setFixedHeight(50)
        label = QLabel('Nuke Path')
        label.setFixedWidth(60)
        self.nuke_path_le = QLineEdit()
        self.btn = QToolButton()
        icon = QIcon()
        icon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon))
        self.btn.setIcon(icon)
        
        self.render_btn = QPushButton('Render...')
        
        main_layout.addWidget(label)
        main_layout.addWidget(self.nuke_path_le)
        main_layout.addWidget(self.btn)
        main_layout.addWidget(self.render_btn)
        
        self.set_signals()
        
    def set_signals(self):
        self.btn.clicked.connect(self.get_nuke_path)
        
    def get_nuke_path(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_path = file_dialog.getOpenFileName(self, 'choose nuke path', '/',
                                                "Nuke File(*.exe)")                                 
        self.nuke_path_le.setText(file_path[0])
        

#-----------------------------------file  widget-----------------------------------#
class AttrLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super(AttrLayout, self).__init__(parent)
        
        self.write_cb = QCheckBox()
        self.write_cb.setChecked(True)
        self.frame_le = QLineEdit()
        self.frame_le.setFixedWidth(80)
        self.dir_le = QLineEdit()
        
        self.addWidget(self.write_cb)
        self.addWidget(self.frame_le)
        self.addWidget(self.dir_le)
        
        
class NukeItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(NukeItem, self).__init__(parent)
        self.name = name

        self.setText(self.name)
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.layout.setAlignment(Qt.AlignTop)
        self.info_browser = QTextBrowser()
        self.init_settings()

    def init_settings(self):
        write_info = get_write_info(self.name)
        if write_info:
            print write_info
            for info in write_info:
                attr_layout = AttrLayout()
                attr_layout.write_cb.setText(info[0])
                attr_layout.frame_le.setText(info[1])
                attr_layout.dir_le.setText(info[2])
                self.layout.addLayout(attr_layout)
                
        
class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent)
        self.nuke_path = nuke_path
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setSortingEnabled(True)
        self.setAcceptDrops(True)
        self.setSpacing(1)
        
    def add_item(self, path):
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
                item = NukeItem(f)
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
            self.add_item(path)
            

class FileWidget(QWidget):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        #main_layout.setContentsMargins(0, 0, 0, 0)
        self.lw = FileListWidget()
        main_layout.addWidget(self.lw)
        

#-----------------------------------attr  widget-----------------------------------#
class AttrWidget(QWidget):
    def __init__(self, parent=None):
        super(AttrWidget, self).__init__(parent)
        self.setFixedHeight(120)
        main_layout = QVBoxLayout(self)
        #main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignTop)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        
        self.layout_of_widget = QStackedLayout(scroll_widget)
        
        main_layout.addWidget(scroll_area)
        

#-----------------------------------attr  widget-----------------------------------#
class InfoWidget(QWidget):
    def __init__(self, parent=None):
        super(InfoWidget, self).__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        self.info_widget = QStackedWidget()
        self.tab_widget.addTab(self.info_widget, 'stdout')
        
        
#-----------------------------------main  widget-----------------------------------#
class MainWidget(QDialog):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle('Nuke Batch Render')
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.resize(700, 400)
        
        main_splitter = QSplitter(Qt.Horizontal)

        main_layout.addWidget(main_splitter)
        
        self.nuke_path_widget = GetNukePathWidget()
        self.file_list_widget = FileWidget()
        self.attr_widget = AttrWidget()
        self.info_widget = InfoWidget()
        
        main_splitter.insertWidget(0, self.file_list_widget)
        main_splitter.setStretchFactor(0, 0)
        
        right_splitter = QSplitter(Qt.Vertical, main_splitter)
        right_splitter.insertWidget(0, self.attr_widget)
        right_splitter.insertWidget(1, self.nuke_path_widget)
        right_splitter.insertWidget(2, self.info_widget)
        right_splitter.setStretchFactor(0, 0)
        
        self.set_signals()
        
    def set_signals(self):
        self.file_list_widget.lw.itemClicked.connect(self.show_attr)
        self.nuke_path_widget.render_btn.clicked.connect(self.do_render)
        
    def show_attr(self, item):
        self.attr_widget.layout_of_widget.addWidget(item.widget)
        self.attr_widget.layout_of_widget.setCurrentWidget(item.widget)
        self.info_widget.info_widget.addWidget(item.info_browser)
        self.info_widget.info_widget.setCurrentWidget(item.info_browser)
    
    def do_render(self):
        pass
        

#-----------------------------------frame  widget-----------------------------------#
class FrameWidget(QFrame):
    def __init__(self, parent=None):
        super(FrameWidget, self).__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Panel|QFrame.Raised)
        

fw = MainWidget()
fw.show()