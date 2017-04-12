import subprocess
from PySide import QtGui, QtCore
import os
import threading
import sys
import json
from datetime import datetime
import collections, cStringIO
from contextlib import closing
import re


path = os.path.abspath(os.path.dirname(__file__))
default_script_path = os.path.join(path, 'nuke_render.py')
default_script_path = default_script_path.replace('\\', '/')

history_path = os.path.join(os.environ['HOME'], 'nuke_batch_render_history.json')


class UniversalAsciiFileFilter(object):

    class Signals(object):
        def __init__(self):
            self._enter   = []
            self._exit    = []
            self._dismiss = []
            self._finish  = []

        @property
        def enter(self):
            return self._enter

        @enter.setter
        def enter(self, value):
            self._enter = value

        @property
        def exit(self):
            return self._exit

        @exit.setter
        def exit(self, value):
            self._exit = value

        @property
        def dismiss(self):
            return self._dismiss

        @dismiss.setter
        def dismiss(self, value):
            self._dismiss = value

        @property
        def finish(self):
            return self._finish

        @finish.setter
        def finish(self, value):
            self._finish = value

    def __init__(self, path = None):
        self._path = path
        self._deque_length = 10
        self.signals = self.Signals()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def check_signals(self, line, signals):
        for signal in signals:
            if isinstance(signal, (list, tuple)):
                result = [sign for sign in signal if not re.match(sign, line)]
                if not any(result): return True
            elif isinstance(signal, basestring): 
                if re.match(signal, line): return True

    def check_deque_is_full(self):
        return len(self._deque) == self._deque_length

    def check_deque_is_empty(self):
        return len(self._deque) == 0

    def execute(self):
        if not self.path: return

        #print "// Processing"
        with closing(cStringIO.StringIO()) as io:
            with open(self.path, "r") as self.infile:
                self._deque = collections.deque(maxlen = self._deque_length)
                prevline, insidedeque, exitingdeque = None, False, False

                for line in self.infile:
                    if not insidedeque:
                        if self.check_signals(line, self.signals.enter):
                            insidedeque, exitingdeque = True, False

                    if self.check_signals(line, self.signals.dismiss): continue

                    if insidedeque:
                        self._deque.append(line)

                        if self.check_signals(line, self.signals.finish):
                            insidedeque, exitingdeque = False, False
                            self._deque.clear()
                            break

                        if self.check_signals(line, self.signals.exit):
                            insidedeque, exitingdeque = False, True

                    if self.check_deque_is_full():
                        prevline = self._deque.popleft()
                        io.write(prevline)

                    elif insidedeque or exitingdeque:
                        if not self.check_deque_is_empty():
                            prevline = self._deque.popleft()
                            io.write(prevline)

                            if exitingdeque:
                                io.write("@ o @\n")

                    else:
                        exitingdeque = False

                if not self.check_deque_is_empty():
                    for line in self._deque:
                        io.write(line)

                    self._deque.clear()

            #print "// Done"
            return io.getvalue()



def get_os_type():
    if sys.platform.startswith('win'):
        os_type = 'windows'
    elif sys.platform.startswith('linux'):
        os_type = 'linux'
    else:
        os_type = 'mac'
    return os_type
    

def get_write_info(nuke_file):
    uaff = UniversalAsciiFileFilter()
    uaff.path = nuke_file
    uaff.signals.enter   = ["Write \{"]
    uaff.signals.exit    = [r"^\}"]
    uaff.signals.dismiss = []
    uaff.signals.finish  = []
    content = uaff.execute()
    write_nodes = content.split('@ o @')
    write_nodes = [node.strip('\n') for node in write_nodes if node.strip('\n')]
    
    f = open(nuke_file, 'r')
    value = f.readlines()
    f.close()
    value = ''.join(value)
    
    pattern_viewer = r'Viewer\s*\{[^{}]*\}'
    pattern_name = 'name ([^\n]*)'
    pattern_file = 'file ([^\n]*)'
    pattern_frame_range = 'frame_range ([^\n]*)'
    
    viewer_nodes = re.findall(pattern_viewer, value)
    frame_range = re.findall(pattern_frame_range, viewer_nodes[0])[0]
    
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
'''
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
'''
        
#-----------------------------------Render Widget-----------------------------------#
class GetPathWidget(QtGui.QWidget):
    def __init__(self, name=None, parent=None):
        super(GetPathWidget, self).__init__(parent)
        self.name = name
        main_layout = QtGui.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QtGui.QLabel(self.name)
        self.label.setFixedWidth(70)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.le = QtGui.QLineEdit()
        self.btn = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon))
        self.btn.setIcon(icon)
        
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.le)
        main_layout.addWidget(self.btn)
        

class RenderWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RenderWidget, self).__init__(parent)
        
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setSpacing(0)
        
        self.script_path_widget = GetPathWidget('script Path')
        self.render_path_widget = GetPathWidget('Nuke Path')
        
        button_layout = QtGui.QHBoxLayout()
        self.render_btn = QtGui.QPushButton('Render...')
        button_layout.addStretch()
        button_layout.addWidget(self.render_btn)
        main_layout.addWidget(self.script_path_widget)
        main_layout.addWidget(self.render_path_widget)
        main_layout.addLayout(button_layout)
        self.set_signals()
        
    def set_signals(self):
        self.script_path_widget.btn.clicked.connect(self.get_script_path)
        self.render_path_widget.btn.clicked.connect(self.get_nuke_path)
        
    def get_script_path(self):
        file_dialog = QtGui.QFileDialog()
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        file_path = file_dialog.getOpenFileName(self, 'choose script path', path,
                                                "Nuke File(*.py)")                                 
        self.script_path_widget.le.setText(file_path[0])
        
    def get_nuke_path(self):
        file_dialog = QtGui.QFileDialog()
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        file_path = file_dialog.getOpenFileName(self, 'choose nuke path', 'C:/Program Files',
                                                "Nuke File(*.exe)")                                 
        self.render_path_widget.le.setText(file_path[0])
         

#-----------------------------------file  widget-----------------------------------#
class AttrLayout(QtGui.QHBoxLayout):
    def __init__(self, parent=None):
        super(AttrLayout, self).__init__(parent)
        
        self.write_cb = QtGui.QCheckBox()
        self.write_cb.setChecked(True)
        self.frame_le = QtGui.QLineEdit()
        self.frame_le.setFixedWidth(80)
        self.dir_le = QtGui.QLineEdit() 
        self.open_btn = QtGui.QPushButton('open')
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
        
        
class NukeItem(QtGui.QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(NukeItem, self).__init__(parent)
        self.name = name
        self.thread = list()
        self.error = False
        
        self.setText(self.name)
        self.widget = None
        self.layout = None
        self.info_browser = None
        self.setForeground(QtCore.Qt.white)
        self.init_settings()

    def init_settings(self):
        self.widget = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout(self.widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.info_browser = QtGui.QTextBrowser()
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
                
        
class FileListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent)
        self.setSelectionMode(QtGui.QListWidget.ExtendedSelection)
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
                file_info = QtCore.QFileInfo(f)
                icon_provider = QtGui.QFileIconProvider ()
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
            

class FileWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(FileWidget, self).__init__(parent)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(3, 8, 3, 8)
        self.menu = QtGui.QMenu()
        self.remove_action = QtGui.QAction('Remove', self)
        self.abort_action = QtGui.QAction('Abort Render', self)
        self.refresh_action = QtGui.QAction('Refresh', self)
        self.lw = FileListWidget()
        main_layout.addWidget(self.lw)
        
    def contextMenuEvent(self, event):
        self.menu.clear()
        self.menu.addAction(self.remove_action)
        self.menu.addAction(self.abort_action)
        self.menu.addAction(self.refresh_action)
        self.menu.exec_(QtGui.QCursor.pos())
        event.accept()
        

#-----------------------------------attr  widget-----------------------------------#
class AttrWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AttrWidget, self).__init__(parent)
        #self.setFixedHeight(95)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        
        scroll_area = QtGui.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        
        scroll_widget = QtGui.QWidget()
        scroll_area.setWidget(scroll_widget)
        
        self.layout_of_widget = QtGui.QStackedLayout(scroll_widget)
        widget = QtGui.QWidget()
        self.layout_of_widget.addWidget(widget)
        
        main_layout.addWidget(scroll_area)
        

#-----------------------------------attr  widget-----------------------------------#
class InfoWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(InfoWidget, self).__init__(parent)
        self.main_layout = QtGui.QVBoxLayout(self)
        self.tab_widget = QtGui.QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        self.info_widget = QtGui.QStackedWidget()
        self.tab_widget.addTab(self.info_widget, 'stdout')
        
        widget = QtGui.QWidget()
        self.info_widget.addWidget(widget)
        
        
#-----------------------------------main  widget-----------------------------------#
class MainWidget(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent) 

        self.setWindowTitle('Nuke Batch Render')
        
        central_widget = QtGui.QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QtGui.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.resize(800, 500)
        
        main_splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        main_splitter.setStretchFactor(1, 1)
        main_splitter.setAutoFillBackground(True)

        main_layout.addWidget(main_splitter)
        
        self.render_widget = RenderWidget()
        self.render_widget.script_path_widget.le.setText(default_script_path)
        self.file_list_widget = FileWidget()
        self.attr_widget = AttrWidget()
        self.info_widget = InfoWidget()
        
        main_splitter.insertWidget(0, self.file_list_widget)

        right_splitter = QtGui.QSplitter(QtCore.Qt.Vertical, main_splitter)
        right_splitter.insertWidget(0, self.attr_widget)
        right_splitter.insertWidget(1, self.render_widget)
        right_splitter.insertWidget(2, self.info_widget)
        
        right_splitter.setStretchFactor(0, 0)
        main_splitter.setSizes([280, 520])
        right_splitter.setSizes([60, 120, 300])
        self.set_signals()
        
    def set_signals(self):
        self.file_list_widget.lw.itemClicked.connect(self.show_attr)
        self.file_list_widget.remove_action.triggered.connect(self.clear_attr_widget)
        self.file_list_widget.abort_action.triggered.connect(self.abort_thread)
        self.file_list_widget.refresh_action.triggered.connect(self.refresh)
        self.render_widget.render_btn.clicked.connect(self.do_render)
        
    def clear_attr_widget(self):
        if self.file_list_widget.lw.selectedItems():
            for item in self.file_list_widget.lw.selectedItems():
                if not item.thread:
                    self.file_list_widget.lw.takeItem(self.file_list_widget.lw.row(item))
                    self.attr_widget.layout_of_widget.setCurrentIndex(0)
                    self.info_widget.info_widget.setCurrentIndex(0)
                else:
                    QtGui.QMessageBox.warning(None, 'Info', 'Please Abort Render First')

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
                    item.setForeground(QtCore.Qt.white)
                self.show_attr(selected_items[0])
                    
    def show_attr(self, item):
        self.attr_widget.layout_of_widget.addWidget(item.widget)
        self.attr_widget.layout_of_widget.setCurrentWidget(item.widget)
        self.info_widget.info_widget.addWidget(item.info_browser)
        self.info_widget.info_widget.setCurrentWidget(item.info_browser)
        
    def show_info(self, value):
        if value[1].startswith('Exception') or 'Error' in value[1][:20]:
            value[0].info_browser.append('<font color=#FF0000>%s</font>' % value[1])
            value[0].setForeground(QtCore.Qt.red)
            value[0].thread = list()
        else:
            value[0].info_browser.append(value[1])
        if value[1].startswith('Total render time'):
            value[0].info_browser.append('<font color=#00FF00><b>Fininshed</font></b>')
        
    def get_command(self):
        commands = list()
        script_path = str(self.render_widget.script_path_widget.le.text())
        nuke_path = str(self.render_widget.render_path_widget.le.text())
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
        commands = self.get_command()
        self.threads = list()
        for command in commands:
            #command[0]:item
            #command[1]:command
            work = Work(command[0], command[1])
            command[0].append_thread(work)
            work.signal.connect(self.show_info)
            work.start()
            self.threads.append(work)

    def read_settings(self):
        if os.path.isfile(history_path):
            f = open(history_path, 'r')
            data = json.loads(f.read())
            f.close()
            self.render_widget.render_path_widget.le.setText(data['render_path'])
            self.render_widget.script_path_widget.le.setText(data['script_path'])
        
    def write_settings(self):
        f = open(history_path, 'w')
        script_path_final = str(self.render_widget.script_path_widget.le.text())
        render_path_final = str(self.render_widget.render_path_widget.le.text())
        data = {'script_path':script_path_final, 'render_path':render_path_final}
        json_data = json.dumps(data)
        f.write(json_data)
        f.close()
        
    def closeEvent(self, event):
        self.write_settings()
            

class Work(QtCore.QThread):
    signal = QtCore.Signal(list)

    def __init__(self, item=None, command=None, parent=None):
        super(Work, self).__init__(parent)
        self.item = item
        self.command = command
        self.finished.connect(self.show_finished_info)
        self.started.connect(self.show_started_info)
        
    def show_finished_info(self):
        current_time = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        self.item.thread = list()
        if not self.item.error:
            self.item.setForeground(QtCore.Qt.green)
            self.item.info_browser.append('<font color=#00FF00><b>%s finish at %s</font></b>' \
                                            % (self.item.name, current_time))
        else:
            self.deleteLater()
        
    def show_started_info(self):
        self.item.setForeground(QtGui.QColor(255, 100, 0))
        current_time = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
        self.item.info_browser.append('<font color=#FF00FF><b>%s start at %s</font></b>' \
                                        % (self.item.name, current_time))
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
        return 

                
def run():
    global nt
    try:
        nt.close()
        nt.deleteLater()
    except:pass
    app = QtGui.qApp
    main_widget = app.activeWindow()
    nt = MainWidget(main_widget)
    nt.read_settings()
    nt.show()