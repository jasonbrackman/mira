import subprocess
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import os
import threading
import re
import sys
import Queue


path = os.path.abspath(os.path.dirname(__file__))
script_path = os.path.join(path, 'nuke_render.py')

history_path = os.path.join(os.environ['HOME'], 'nuke_batch_render_history.txt')


def get_os_type():
    if sys.platform.startswith('win'):
        os_type = 'windows'
    elif sys.platform.startswith('linux'):
        os_type = 'linux'
    else:
        os_type = 'mac'
    return os_type


def re_group(file_list, n):
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
        
        self.spin = QSpinBox()
        self.spin.setRange(1, 10)
        self.render_btn = QPushButton('Render...')
        
        main_layout.addWidget(label)
        main_layout.addWidget(self.nuke_path_le)
        main_layout.addWidget(self.btn)
        main_layout.addWidget(self.spin)
        main_layout.addWidget(self.render_btn)
        
        self.set_signals()
        
    def set_signals(self):
        self.btn.clicked.connect(self.get_nuke_path)
        
    def get_nuke_path(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_path = file_dialog.getOpenFileName(self, 'choose nuke path', 'C:/Program Files',
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
        self.open_btn = QPushButton('open')
        self.open_btn.setFixedWidth(40)
        
        self.addWidget(self.write_cb)
        self.addWidget(self.frame_le)
        self.addWidget(self.dir_le)
        self.addWidget(self.open_btn)
        self.set_signals()
        
    def set_signals(self):
        self.open_btn.clicked.connect(self.open_dir)
        
    def open_dir(self):
        path = self.dir_le.text()
        if path:
            try:
                if get_os_type() == 'windows':
                    os.startfile(os.path.dirname(path))
                elif get_os_type() == 'linux':
                    os.system('xdg-open %s' % path)
            except:pass
        
        
class NukeItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(NukeItem, self).__init__(parent)
        self.name = name
        self.thread = list()
        self.error = False
        
        self.setText(self.name)
        self.widget = None
        self.layout = None
        self.info_browser = None
        self.setForeground(Qt.white)
        self.init_settings()

    def init_settings(self):
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.layout.setAlignment(Qt.AlignTop)
        self.info_browser = QTextBrowser()
        write_info = get_write_info(self.name)
        if write_info:
            #print write_info
            for info in write_info:
                attr_layout = AttrLayout()
                attr_layout.write_cb.setText(info[0])
                attr_layout.frame_le.setText(info[1])
                attr_layout.dir_le.setText(info[2])
                self.layout.addLayout(attr_layout)
                
    def append_thread(self, thread):
        self.thread.append(thread)
                
        
class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent)
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
        if os.path.isfile(path) and os.path.splitext(path)[-1] == '.nk':
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
                file_info = QFileInfo(f)
                icon_provider = QFileIconProvider ()
                icon = icon_provider.icon(file_info )
                item = NukeItem(f)
                item.setIcon(icon)
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
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            self.add_item(path)
            

class FileWidget(QWidget):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        self.menu = QMenu()
        self.remove_action = QAction('Remove', self)
        self.abort_action = QAction('Abort Render', self)
        self.refresh_action = QAction('Refresh', self)
        self.lw = FileListWidget()
        main_layout.addWidget(self.lw)
        
    def contextMenuEvent(self, event):
        self.menu.clear()
        self.menu.addAction(self.remove_action)
        self.menu.addAction(self.abort_action)
        self.menu.addAction(self.refresh_action)
        self.menu.exec_(QCursor.pos())
        event.accept()
        

#-----------------------------------attr  widget-----------------------------------#
class AttrWidget(QWidget):
    def __init__(self, parent=None):
        super(AttrWidget, self).__init__(parent)
        self.setFixedHeight(95)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        
        self.layout_of_widget = QStackedLayout(scroll_widget)
        widget = QWidget()
        self.layout_of_widget.addWidget(widget)
        
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
        
        widget = QWidget()
        self.info_widget.addWidget(widget)
        
        
#-----------------------------------main  widget-----------------------------------#
class MainWidget(QMainWindow):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent) 

        self.setWindowTitle('Nuke Batch Render')
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.resize(800, 500)
        
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
        self.file_list_widget.remove_action.triggered.connect(self.clear_attr_widget)
        self.file_list_widget.abort_action.triggered.connect(self.abort_thread)
        self.file_list_widget.refresh_action.triggered.connect(self.refresh)
        self.nuke_path_widget.render_btn.clicked.connect(self.do_render)
        
    def clear_attr_widget(self):
        if self.file_list_widget.lw.selectedItems():
            for item in self.file_list_widget.lw.selectedItems():
                if not item.thread:
                    self.file_list_widget.lw.takeItem(self.file_list_widget.lw.row(item))
                    self.attr_widget.layout_of_widget.setCurrentIndex(0)
                    self.info_widget.info_widget.setCurrentIndex(0)
                else:
                    QMessageBox.warning(None, 'Info', 'Please Abort Render First')

    def abort_thread(self):
        if self.file_list_widget.lw.selectedItems():
            for item in self.file_list_widget.lw.selectedItems():
                if item.thread:
                    for thread in item.thread:
                        thread.terminate()
                    item.thread = list()
                    
    def refresh(self):
        selected_items = self.file_list_widget.lw.selectedItems()
        if selected_items:
            selected_items = [item for item in selected_items if not item.thread]
            if selected_items:
                for item in selected_items:
                    self.attr_widget.layout_of_widget.removeWidget(item.widget)
                    self.info_widget.info_widget.removeWidget(item.info_browser)
                    item.init_settings()
                    item.setForeground(Qt.white)
                self.show_attr(selected_items[0])
                    
    def show_attr(self, item):
        self.attr_widget.layout_of_widget.addWidget(item.widget)
        self.attr_widget.layout_of_widget.setCurrentWidget(item.widget)
        self.info_widget.info_widget.addWidget(item.info_browser)
        self.info_widget.info_widget.setCurrentWidget(item.info_browser)
        
    def show_info(self, value):
        if value[1].startswith('Exception') or \
           value[1].startswith('RuntimeError') or \
           value[1].startswith('AttributeError')or \
           value[1].startswith('ValueError') or\
           value[1].startswith('TypeError') or\
           value[1].startswith('KeyError') or\
           value[1].startswith('IndexError') or\
           value[1].startswith('NameError'):
            value[0].info_browser.append('<font color=#FF0000>%s</font>' % value[1])
            value[0].setForeground(Qt.red)
            value[0].thread = list()
        else:
            value[0].info_browser.append(value[1])
        
    def get_command(self):
        commands = list()
        nuke_path = str(self.nuke_path_widget.nuke_path_le.text())
        selected_items = self.file_list_widget.lw.selectedItems()
        if nuke_path and selected_items:
            for item in selected_items:
                nuke_file = str(item.name)
                for i in xrange(item.layout.count()):
                    layout = item.layout.itemAt(i)
                    if layout.write_cb.isChecked():
                        temp = list()
                        write_node = str(layout.write_cb.text())
                        frame_range = str(layout.frame_le.text())
                        output_path = str(layout.dir_le.text())
                        command = "\"%s\" -t %s %s %s %s %s" \
                        % (nuke_path, script_path, nuke_file, write_node, frame_range, output_path)
                        temp.append([item, command])
                        commands.extend(temp)
        return commands
                    
    def do_render(self):
        queue = Queue.Queue()
        commands = self.get_command()
        print commands
        '''
        self.threads = list()
        for command in commands:
            #command[0]:item
            #command[1]:command
            work = Work(command[0], command[1])
            command[0].append_thread(work)
            work.signal.connect(self.show_info)
            work.start()
            self.threads.append(work)
        '''
        
        for command in commands:
            queue.put(command)
        
        self.threads = list()
        while not queue.empty():
            for i in xrange(2):
                work = Work(queue)
                work.start()
                self.threads.append(work)
               
            queue.join()


    def read_settings(self):
        if os.path.isfile(history_path):
            f = open(history_path, 'r')
            value = f.read()
            self.nuke_path_widget.nuke_path_le.setText(value)
            f.close()
        
    def write_settings(self):
        f = open(history_path, 'w')
        f.write(str(self.nuke_path_widget.nuke_path_le.text()))
        f.close()
        
    def closeEvent(self, event):
        self.write_settings()
            

class Work(QThread):
    signal = Signal(list)

    def __init__(self, queue, parent=None):
        super(Work, self).__init__(parent)
        self.queue = queue
        if not self.queue.empty():
            self.item, self.command = self.queue.get()
        
        self.finished.connect(self.show_finished_info)
        self.started.connect(self.show_started_info)
        
    def show_finished_info(self):
        self.item.thread = list()
        if not self.item.error:
            self.item.setForeground(Qt.green)
            self.item.info_browser.append('<font color=#00FF00><b>%s finished</font></b>' % self.item.name)
        else:
            self.deleteLater()
        
    def show_started_info(self):
        self.item.setForeground(QColor(255, 100, 0))
        self.item.info_browser.append('<font color=#00FF00><b>%s started</font></b>' % self.item.name)
        self.item.info_browser.append('<font color=#00FFFF><b>%s </font></b>' % self.command)
    
    def run(self):
        p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            ret_code = p.poll()
            if ret_code == 0:
                break
            elif ret_code == 1:
                self.item.error = True
                self.item.thread = list()
                self.item.info_browser.append('<font color=#FF0000>nuke was terminated for some reason<font>')
                self.terminate()
                break
            elif ret_code != None:
                self.item.error = True
                self.item.thread = list()
                self.item.info_browser.append('<font color=#FF0000>%s<font>' % ret_code)
                self.terminate()
                break
            line = p.stdout.readline()
            if line.strip() and not line.startswith('.'):
                self.signal.emit([self.item, line.strip()])
        
        self.queue.task_done()
        
            
                
def run():
    global nt
    try:
        nt.close()
        nt.deleteLater()
    except:pass
    app = qApp
    main_widget = app.activeWindow()
    nt = MainWidget(main_widget)
    nt.read_settings()
    nt.show()