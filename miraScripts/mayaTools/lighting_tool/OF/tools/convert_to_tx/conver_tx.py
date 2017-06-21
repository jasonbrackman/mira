from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import threading
import os
import sys
import atexit

#path = os.path.abspath(os.path.dirname(__file__))
path = os.path.abspath(os.path.dirname(sys.argv[0]))
qss_path = os.path.join(path, 'style.qss')

maketx_win = r'C:/mnt/centralized_tool/Software/mtoadeploy/1.1.2.1/2014/bin/maketx.exe'
maketx_linux = r'/mnt/v/Barajoun_Bilal_CG/software/development/productionTools/solidangle/mtoa/2014_1.1.2.2/bin/maketx'

                        
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
        
        
def transform_texture(texture_list):
    for texture in texture_list:
        if get_os_type() == 'windows':
            os.system("%s -v %s" % (maketx_win, texture))
        if get_os_type() == 'linux':
            os.system("%s -v %s" % (maketx_linux, texture))
        print "[OF] info:%s has been transformed" % texture

    
class ConvertTx(QDialog):
    def __init__(self, parent=None):
        super(ConvertTx, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        self.setWindowTitle('Convert to TX')
        self.setWindowIcon(QIcon(os.path.join(path, 'icon.ico')))
        self.setStyleSheet(open(qss_path, 'r').read())
        self.resize(500, 300)
        #---------------------------------------------------------#
        label_layout = QHBoxLayout()
        label = QLabel()
        label.setText('<font color="#00FF00" size=4><b>Convert these files to (.tx)</b> </font>')
        self.update_btn = QToolButton()
        self.update_btn.setIcon(QIcon(os.path.join(path, 'update.png')))
        self.update_btn.setStyleSheet('QToolButton{background-color: transparent}')
        label_layout.addWidget(label)
        label_layout.addWidget(self.update_btn)
        #---------------------------------------------------------#
        self.list_widget = DropListWidget()
        #---------------------------------------------------------#
        button_layout = QHBoxLayout()
        self.clear_btn = QPushButton('Clear')
        self.remove_btn = QPushButton('Remove')
        self.dis_select_btn = QPushButton('Diselect')
        self.spin_box = QSpinBox()
        self.spin_box.setStyleSheet('QSpinBox{background-color:#222222}')
        self.spin_box.setRange(1, 10)
        self.transform_btn = QPushButton('Transform')
        button_layout.addStretch()
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.remove_btn)
        button_layout.addWidget(self.dis_select_btn)
        button_layout.addWidget(self.spin_box)
        button_layout.addWidget(self.transform_btn)
        #---------------------------------------------------------#
        main_layout.addLayout(label_layout)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(button_layout)
        #---------------------------------------------------------#
        self.set_background()
        self.set_signals()
        
    def set_signals(self):
        self.clear_btn.clicked.connect(self.do_clear)
        self.dis_select_btn.clicked.connect(self.diselect_all)
        self.remove_btn.clicked.connect(self.do_remove)
        self.transform_btn.clicked.connect(self.do_transform)
        self.update_btn.clicked.connect(self.update)
        
    def set_background(self):
        image_path = os.path.join(path, 'tx.png')
        self.image = QImage(image_path)
        palette = QPalette()
        palette.setBrush(QPalette.Background,
                        QBrush(self.image.scaled(self.size(),
                                                       Qt.IgnoreAspectRatio,
                                                       Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        palette = QPalette()
        palette.setBrush(QPalette.Background,
                         QBrush(self.image.scaled(event.size(),
                                                        Qt.IgnoreAspectRatio,
                                                        Qt.SmoothTransformation)))
        self.setPalette(palette)
        
    def do_clear(self):
        self.list_widget.clear()
        
    def do_remove(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            for selected_item in selected_items:
                self.list_widget.takeItem(self.list_widget.row(selected_item))
                
    def diselect_all(self):
        for i in xrange(self.list_widget.count()):
            self.list_widget.item(i).setSelected(False)
            
    def do_transform(self):
        all_textures = [str(i.text()) for i in self.list_widget.selectedItems()]
        if all_textures:
            all_textures_grp = re_group(all_textures, int(self.spin_box.value()))
            threads = []
            for texture_list in all_textures_grp:
                t = threading.Thread(target=transform_texture, args=(texture_list, ))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        self.update()
                
    def update(self):
        for selected_item in self.list_widget.selectedItems():
            old_file = str(selected_item.text())
            new_file = os.path.splitext(old_file)[0] + '.tx'
            if os.path.isfile(new_file):
                self.list_widget.takeItem(self.list_widget.row(selected_item))
                
    def  mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()
        

class DropListWidget(QListWidget):
    def __init__(self, parent=None):
        super(DropListWidget, self).__init__(parent)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setSortingEnabled(True)
        self.setSpacing(1)
        self.setAcceptDrops(True)
        self.setStyleSheet('QListWidget{border: 1px solid #111111;\
                                        background-color: transparent;\
                                        color: #CCCCCC}')
        
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
        exist_item = []
        if self.count():
            for x in xrange(self.count()):
                exist_item.append(str(self.item(x).text()))
        all_files = []
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            if os.path.isfile(path) and os.path.splitext(path)[-1] not in ['.tx', '.db', '.mb', '.ma', '.exe']:
                if exist_item:
                    if path.replace('\\', '/') not in exist_item:
                        all_files.append(path)
                else:
                    all_files.append(path)
            if os.path.isdir(path):
                files = [os.path.join(path, file) for file in os.listdir(path) 
                                                    if file != '.mayaSwatches' 
                                                    and not os.path.isdir(os.path.join(path, file))
                                                    and os.path.splitext(file)[-1] not in ['.tx', '.db', '.mb', '.ma', '.exe']]
                files = [file.replace('\\', '/') for file in files]
                if exist_item:
                    for file in files:
                        if file not in exist_item:
                            all_files.append(file)
                else:
                    all_files.extend(files)
        for file in all_files:
            item = QListWidgetItem(file)
            item.setIcon(QIcon(file))
            self.addItem(item)
                    

def main():
    app = QApplication(sys.argv)
    ct = ConvertTx()
    ct.show()
    app.exec_()

if __name__ == '__main__':
    main()