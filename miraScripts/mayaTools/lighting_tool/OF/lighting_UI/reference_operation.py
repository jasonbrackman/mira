import maya.cmds as mc
import maya.mel as mel
from PySide import QtGui, QtCore
import sys
import os


class MayaUtility(object):
    @staticmethod
    def get_maya_win():
        import maya.OpenMayaUI as mui
        main_window = None
        ptr = mui.MQtUtil.mainWindow()
        if 'PyQt4' in QtGui.__name__:
            import sip
            main_window = sip.wrapinstance(long(ptr), QtCore.QWidget)
        elif 'PySide' in QtGui.__name__:
            import shiboken
            main_window = shiboken.wrapInstance(long(ptr), QtGui.QWidget)
        return main_window

    def get_os_type(self):
        if sys.platform.startswith('win'):
            os_type = 'windows'
        elif sys.platform.startswith('linux'):
            os_type = 'linux'
        else:
            os_type = 'mac'
        return os_type

    def get_all_ref(self):
        all_ref = mc.ls(type='reference')
        all_ref = [ref for ref in all_ref if 'sharedReferenceNode' not in ref]
        return all_ref
        
    def get_ref_by_obj(self):
        selected_objects = mc.ls(sl=1)
        if selected_objects:
            ref_node_names = [mc.referenceQuery(obj, referenceNode=1, topReference=1)
                              for obj in selected_objects
                              if mc.referenceQuery(obj, isNodeReferenced=1)]
            ref_node_names = list(set(ref_node_names))
            # if not mc.window('referenceEditorPanel1Window', ex=1):
            #     mc.ReferenceEditor()
            # ref_panel = mel.eval("$gReferenceEditorPanel = $gReferenceEditorPanel")
            # all_ref = self.get_all_ref()
            # for index, ref in enumerate(all_ref):
            #     mc.sceneEditor(ref_panel, e=1, si=index)
            #     sel_ref = mc.sceneEditor(ref_panel, q=1, selectReference=1)
            #     if sel_ref[0] == ref_node_names[0]:
            #         break
            return ref_node_names
        else:
            print '[OF] info: Nothing Selected!'
    
    def get_obj_by_ref(self, ref_nodes):
        all_transforms = list()
        for ref_node in ref_nodes:
            child_ref_nodes = self.get_child_ref(ref_node)
            if child_ref_nodes:
                for child in child_ref_nodes:
                    all_objs = mc.referenceQuery(child, dagPath=1, nodes=1)
                    transforms = mc.ls(all_objs, type='transform')
                    all_transforms.extend(transforms)
            else:
                all_objs = mc.referenceQuery(ref_node, dagPath=1, nodes=1)
                transforms = mc.ls(all_objs, type='transform')
                all_transforms.extend(transforms)
        if all_transforms:
            all_transforms = list(set(all_transforms))
            mc.select(all_transforms, r=1)
            
    def remove_ref(self, ref_node):
        if not self.get_parent_ref(ref_node):
            file_name = self.get_file_name(ref_node)
            mc.file(file_name, rr=1)
        else:
            print '[OF] info: This reference cannot be removed since its parent is a reference.'
        
    def remove_unload_ref(self):
        all_ref = mc.file(q=1, r=1)
        if all_ref:
            for ref in all_ref:
                a = mc.referenceQuery(ref, isLoaded=1)
                if not a:
                    mc.file(ref, removeReference=1)

    def import_loaded_ref(self):
        all_ref = mc.file(q=1, r=1)
        if all_ref:
            for ref in all_ref:
                a = mc.referenceQuery(ref, isLoaded=1)
                if a:
                    mc.file(ref, importReference=1)
        try:
            self.import_loaded_ref()
        except:pass
        
    def check_loaded(self, ref_node):
        result = mc.referenceQuery(ref_node, isLoaded=1)
        return result
        
    def get_file_name(self, ref_node):
        file_name = mc.referenceQuery(ref_node, filename=1)
        return file_name
        
    def get_all_ref_list(self):
        all_ref = self.get_all_ref()
        all_ref_list = [[ref, self.get_file_name(ref)] for ref in all_ref]
        return all_ref_list
        
    def get_all_top_reference(self):
        all_top_ref_file = mc.file(q=1, r=1)
        all_top_ref_node = [mc.referenceQuery(ref, referenceNode=1) for ref in all_top_ref_file]
        return all_top_ref_node
         
    def get_child_ref(self, ref_node):
        return mc.referenceQuery(ref_node, child=1, referenceNode=1)

    def get_parent_ref(self, ref_node):
        return mc.referenceQuery(ref_node, parent=1, referenceNode=1)

    def import_reference(self, ref_node):
        file_name = self.get_file_name(ref_node)
        mc.file(file_name, importReference=1)
        
    def load_reference(self, ref_node):
        file_name = self.get_file_name(ref_node)
        mc.file(file_name, loadReference=1)
        
    def unload_reference(self, ref_node):
        file_name = self.get_file_name(ref_node)
        mc.file(file_name, unloadReference=1)

        
class ReferenceTree(QtGui.QTreeView):

    def __init__(self, parent=None):
        super(ReferenceTree, self).__init__(parent)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtGui.QTreeView.ExtendedSelection)
        self.menu = QtGui.QMenu()
        self.import_action = QtGui.QAction('import Objects From Reference', self)
        self.remove_action = QtGui.QAction('Remove Reference', self)
        self.select_action = QtGui.QAction('Select Polygon', self)
        self.load_action = QtGui.QAction('Load Reference', self)
        self.unload_action = QtGui.QAction('Unload Reference', self)
        self.open_action = QtGui.QAction('Open Direction', self)

    def contextMenuEvent(self, event):
        self.menu.clear()
        self.menu.addAction(self.import_action)
        self.menu.addSeparator()
        self.menu.addAction(self.remove_action)
        self.menu.addSeparator()
        self.menu.addAction(self.select_action)
        self.menu.addSeparator()
        self.menu.addAction(self.load_action)
        self.menu.addAction(self.unload_action)
        self.menu.addSeparator()
        self.menu.addAction(self.open_action)
        self.menu.exec_(QtGui.QCursor.pos())
        event.accept()


class ReferenceItem(QtGui.QStandardItem):
    def __init__(self, text=None, color=QtCore.Qt.white, bold=False, font_size=10):
        super(ReferenceItem, self).__init__()
        self.text = text
        self.setText(self.text)
        self.setForeground(color)
        font = QtGui.QFont()
        font.setPointSizeF(font_size)
        if bold:
            font.setWeight(QtGui.QFont.Bold)
        self.setData(font, QtCore.Qt.FontRole)
        self.setEditable(False)

    def set_color(self, arg):
        self.setForeground(arg)


class ReferenceView(QtGui.QDialog):
    utility = MayaUtility()

    def __init__(self, parent=None):
        super(ReferenceView, self).__init__(parent)
        self.setObjectName('Reference Editor')
        self.setWindowTitle('Reference Editor')
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.resize(600, 400)

        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.tree_view = ReferenceTree()
        self.tree_view.resizeColumnToContents(0)
        self.tree_view.resizeColumnToContents(1)
        self.model = QtGui.QStandardItemModel()

        button_layout = QtGui.QHBoxLayout()
        self.refresh_btn = QtGui.QPushButton('Refresh')
        self.select_btn = QtGui.QPushButton('Select Reference By Object')
        self.remove_all_btn = QtGui.QPushButton('Remove All Unloaded Reference')
        self.import_all_btn = QtGui.QPushButton('Import All Loaded Reference')
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.select_btn)
        button_layout.addWidget(self.remove_all_btn)
        button_layout.addWidget(self.import_all_btn)

        main_layout.addWidget(self.tree_view)
        main_layout.addLayout(button_layout)
        self.set_model()
        self.set_signals()

    def set_signals(self):
        self.tree_view.import_action.triggered.connect(self.do_import)
        self.tree_view.remove_action.triggered.connect(self.do_remove)
        self.tree_view.select_action.triggered.connect(self.do_select)
        self.tree_view.load_action.triggered.connect(self.do_load)
        self.tree_view.unload_action.triggered.connect(self.do_unload)
        self.tree_view.open_action.triggered.connect(self.open_dir)
        self.refresh_btn.clicked.connect(self.set_model)
        self.remove_all_btn.clicked.connect(self.remove_all_unloaded)
        self.import_all_btn.clicked.connect(self.import_all_loaded)
        self.select_btn.clicked.connect(self.select_reference)

    def set_model(self):
        self.model.clear()
        header_list = ['Reference Node', 'Reference File Name']
        self.model.setHorizontalHeaderLabels(header_list)
        all_top_ref = self.utility.get_all_top_reference()
        for ref in all_top_ref:
            ref_node_item = ReferenceItem(ref)
            ref_file_name = self.utility.get_file_name(ref)
            ref_file_item = ReferenceItem(ref_file_name)
            load_status = self.utility.check_loaded(ref)
            if not load_status:
                ref_node_item.set_color(QtCore.Qt.red)
                ref_file_item.set_color(QtCore.Qt.red)
            self.model.appendRow([ref_node_item, ref_file_item])
            child_ref = self.utility.get_child_ref(ref)
            if child_ref:
                for child in child_ref:
                    child_item = ReferenceItem(child)
                    child_file_name = self.utility.get_file_name(child)
                    child_file_item = ReferenceItem(child_file_name)
                    load_status = self.utility.check_loaded(child)
                    if not load_status:
                        child_item.set_color(QtCore.Qt.red)
                        child_file_item.set_color(QtCore.Qt.red)
                    ref_node_item.appendRow([child_item, child_file_item])
        self.tree_view.setModel(self.model)
        self.tree_view.expandAll()

    def get_selected_ref_nodes(self):
        selected_ref_nodes = [self.model.itemFromIndex(i).text
                              for i in self.tree_view.selectedIndexes()
                              if i.column() == 0]
        return selected_ref_nodes

    def do_import(self):
        selected_ref_nodes = self.get_selected_ref_nodes()
        if selected_ref_nodes:
            for ref in selected_ref_nodes:
                if self.utility.check_loaded(ref):
                    self.utility.import_reference(ref)
            self.set_model()

    def do_remove(self):
        selected_ref_nodes = self.get_selected_ref_nodes()
        if selected_ref_nodes:
            for ref in selected_ref_nodes:
                self.utility.remove_ref(ref)
            self.set_model()

    def do_select(self):
        selected_ref_nodes = self.get_selected_ref_nodes()
        if selected_ref_nodes:
            self.utility.get_obj_by_ref(selected_ref_nodes)

    def do_load(self):
        selected_ref_nodes = self.get_selected_ref_nodes()
        if selected_ref_nodes:
            for ref in selected_ref_nodes:
                self.utility.load_reference(ref)
            self.set_model()

    def do_unload(self):
        selected_ref_nodes = self.get_selected_ref_nodes()
        if selected_ref_nodes:
            for ref in selected_ref_nodes:
                self.utility.unload_reference(ref)
            self.set_model()

    def open_dir(self):
        selected_ref_nodes = self.get_selected_ref_nodes()
        if selected_ref_nodes:
            for ref in selected_ref_nodes:
                file_name = self.utility.get_file_name(ref)
                direction = os.path.dirname(file_name)
                if os.path.isdir(direction):
                    if self.utility.get_os_type() == 'windows':
                        os.startfile(direction)
                    elif self.utility.get_os_type() == 'linux':
                        os.system('xdg-open %s' % direction)

    def remove_all_unloaded(self):
        self.utility.remove_unload_ref()
        self.set_model()

    def import_all_loaded(self):
        self.utility.import_loaded_ref()
        self.set_model()

    def select_reference(self):
        self.tree_view.selectionModel().select(QtGui.QItemSelection(), QtGui.QItemSelectionModel.Clear)
        ref_names = self.utility.get_ref_by_obj()
        if ref_names:
            for i in xrange(self.model.rowCount()):
                model_index = self.model.index(i, 0)
                item = self.model.itemFromIndex(model_index)
                if item.text in ref_names:
                    #self.tree_view.setCurrentIndex(model_index)
                    self.tree_view.selectionModel().select(model_index, QtGui.QItemSelectionModel.Select)
                    model_index_1 = self.model.index(i, 1)
                    self.tree_view.selectionModel().select(model_index_1, QtGui.QItemSelectionModel.Select)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.close()


def main():
    global view
    try:
        view.close()
        view.deleteLater()
    except:pass
    main_window = MayaUtility.get_maya_win()
    view = ReferenceView(main_window)
    view.show()

if __name__ == '__main__':
    main()