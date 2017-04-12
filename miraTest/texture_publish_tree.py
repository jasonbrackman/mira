# -*- coding: utf-8 -*-
import copy
import os
import pymel.core as pm
from PySide import QtCore, QtGui
from ui_elements.loadui import loadUiType
from pixoMaya.base import getMayaWindow
import pixoLibs.pixoFileTools as pft
import pixoConfig

uiFileName = "texture_publish_tool.ui"
uiFile = os.path.join(pixoConfig.UI_DIR, uiFileName)  # The .ui file to load
form, base = loadUiType(uiFile)


def get_texture_data():
    texture_data_dict = dict()
    for file_node in pm.ls(type="file"):
        file_texture_name = file_node.fileTextureName.get()
        if file_texture_name not in texture_data_dict:
            texture_data_dict[file_texture_name] = dict()
            texture_data_dict[file_texture_name]["file"] = list()
        if file_node not in texture_data_dict[file_texture_name]["file"]:
            file_node_dict = dict()
            file_node_dict["name"] = file_node.name()
            meshes = get_meshes_by_file_node(file_node)
            meshes = list(set(meshes))
            file_node_dict["mesh"] = list()
            if meshes:
                for mesh in meshes:
                    mesh_dict = dict()
                    udim = get_udim_by_mesh(mesh)
                    mesh_dict["name"] = mesh.name()
                    mesh_dict["udim"] = udim
                    file_node_dict["mesh"].append(mesh_dict)
            texture_data_dict[file_texture_name]["file"].append(file_node_dict)
    return texture_data_dict


def get_meshes_by_file_node(file_node):
    meshes = []
    SGs = pm.ls(file_node.history(future=1, allConnections=1), type="shadingEngine")
    for SG in SGs:
        if SG.inputs(type="mesh"):
            meshes.extend(SG.inputs(type="mesh"))
    return meshes


def get_udim_by_mesh(mesh):
    if not mesh:
        return
    if not mesh.getUVSetNames():
        return
    # if geometry selected, convert to uv and return value
    udims = []
    try:
        uvlist = mesh.getShape().getUVs()
        # get the udims
        rebuilt_uvlist = zip(uvlist[0], uvlist[1])
        for uValue, vValue in rebuilt_uvlist:
            ud = 1000 + 10 * int(vValue) + int(uValue) + 1
            if ud not in udims:
                udims.append(ud)
    except:
        pass
    return udims


class Node(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = list()
        self._parent = parent
        if parent:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    @property
    def name(self):
        return self._name

    def child(self, row):
        return self._children[row]

    @property
    def childCount(self):
        return len(self._children)

    @property
    def parent(self):
        return self._parent

    @property
    def row(self):
        if self._parent:
            return self._parent._children.index(self)

    def isValid(self):
        return False


class TextureNode(Node):
    def __init__(self, name, parent=None):
        super(TextureNode, self).__init__(name, parent)
        self.__chanel = None
        self.__udim = None

    @property
    def node_type(self):
        return "texture"

    @property
    def chanel(self):
        return self.__chanel

    @chanel.setter
    def chanel(self, value):
        if isinstance(value, basestring):
            self.__chanel = value

    @property
    def udim(self):
        return self.__udim

    @udim.setter
    def udim(self, value):
        self.__udim = value

    @property
    def publish_paths(self):
        return self.get_pub_path()

    def get_pub_path(self):
        scene = pm.sceneName()
        try:
            obj = pft.PathDetails.parse_path(scene)
            tex_obj = obj.getRenderPathObject()
            tex_obj.task = 'txt'
            ext = os.path.splitext(self.name)[-1]
            tex_obj.ext = ext[1:]
            tex_obj.render_layer = self.__chanel
            all_pub_path = []
            for each_udim in self.udim:
                tex_obj.framerange = each_udim
                all_pub_path.append(tex_obj.getFullPath())
            return all_pub_path
        except:
            return ""


class FileNode(Node):
    def __init__(self, name, parent=None):
        super(FileNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "file"


class MeshNode(Node):
    def __init__(self, name, parent=None):
        super(MeshNode, self).__init__(name, parent)
        self.__udim = None

    @property
    def node_type(self):
        return "mesh"

    @property
    def udim(self):
        return self.__udim

    @udim.setter
    def udim(self, value):
        self.__udim = value


class TexturePublishToolGUI(form, base):
    def __init__(self, parent=None):
        super(TexturePublishToolGUI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle("Texture Publish tool")
        # list all texture nodes
        self.root_node = None
        self.init_model()
        # Model and delegate
        self._model = TextureTreeModel(self.root_node)   # init the source model
        self._chanel_delegate = ChanelEditDelegate(self.data_view)
        self._publish_delegate = PublishButtonDelegate(self.data_view)
        self.data_view.setItemDelegateForColumn(1, self._chanel_delegate)
        self.data_view.setItemDelegateForColumn(3, self._publish_delegate)
        # contextMenu
        self.data_view.addAction(self.EditSelectedChanelsAction)
        # proxy Model
        self._proxyModel = QtGui.QSortFilterProxyModel()
        self._proxyModel.setSourceModel(self._model)
        self._proxyModel.setDynamicSortFilter(True)
        self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.data_view.setModel(self._proxyModel)
        self.data_view.setSortingEnabled(True)

        # default configs
        self.data_view.resizeColumnToContents(0)
        self.data_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)     # select rows
        self.data_view.setSelectionMode(QtGui.QTreeView.ExtendedSelection)
        # self.data_view.expandAll()
        # show button delegate
        self.show_button_delegate()
        # resize coulumns
        column_width_list = [500, 120, 120, 80]
        for column in range(4):
            self.data_view.setColumnWidth(column, column_width_list[column])
        # connect filter
        self.filter.textChanged.connect(self._proxyModel.setFilterRegExp)   # validate the filter
        self.filter.textChanged.connect(self.show_button_delegate)
        self.EditSelectedChanelsAction.triggered.connect(self.batch_edit_chanels)
        self.referesh_btn.clicked.connect(self.update)
        self.publish_all_btn.clicked.connect(self.publish_all)

    def init_model(self):
        all_textures = get_texture_data()
        self.root_node = Node("publish")
        for texture in all_textures:
            texture_node = TextureNode(texture, self.root_node)
            texture_node.udim = list()
            for each_file in all_textures[texture]["file"]:
                file_node = FileNode(each_file["name"], texture_node)
                meshes = each_file["mesh"]
                if meshes:
                    for mesh in meshes:
                        mesh_node = MeshNode(mesh["name"], file_node)
                        mesh_node.udim = mesh["udim"]
                        if mesh_node.udim:
                            texture_node.udim.extend(mesh_node.udim)
                            texture_node.udim = list(set(texture_node.udim))

    def show_button_delegate(self):
        for i in xrange(self._proxyModel.rowCount()):
            self.data_view.openPersistentEditor(self._proxyModel.index(i, 3))

    def update(self):
        """
        refresh the GUI.
        """
        # It's ugly as I don't have any better idea.
        run_maya()
        self.deleteLater()

    @QtCore.Slot()
    def batch_edit_chanels(self):
        # get selected rows
        proxy_indexs = self.data_view.selectedIndexes()
        selected_rows = list(set([self._proxyModel.mapToSource(i).row() for i in proxy_indexs]))
        # pop a dialog
        value, ok = QtGui.QInputDialog.getText(self, "Edit Chanel", "Enter a Chanel name:", QtGui.QLineEdit.Normal, "")
        if ok:
            # set all
            for row in selected_rows:
                current_index = self._model.index(row, 1, self.root_node)
                self._model.setData(current_index, value, QtCore.Qt.EditRole)

    @QtCore.Slot()
    def publish_all(self):
        print self._model.all_data      # todo: publish all function should be here


class TextureTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        super(TextureTreeModel, self).__init__(parent)
        self._root_node = root

    def rowCount(self, parent):
        if not parent.isValid():
            parent_node = self._root_node
        else:
            parent_node = parent.internalPointer()
        return parent_node.childCount

    def columnCount(self, parent):
        return 4

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name
            if index.column() == 1 and node.node_type == "texture":
                return node.chanel
            if index.column() == 2 and node.node_type in ["texture", "mesh"]:
                if node.udim:
                    udims = [str(udim) for udim in node.udim]
                    return ",".join(udims)
                return "None"

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        node = index.internalPointer()
        if role == QtCore.Qt.EditRole:
            if index.column() == 1 and node.node_type == "texture":
                node.chanel = value
                return True
        return False

    def headerData(self, section, orientation, role):
        header_labels = ["File Path", "Chanel", "UDIMs", "Publish"]
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return header_labels[section]

    def flags(self, index):
        flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        node = index.internalPointer()
        if index.column() == 1 and node.node_type == "texture":
            flags = flags | QtCore.Qt.ItemIsEditable
        return flags

    def parent(self, index):
        node = index.internalPointer()
        parent_node = node.parent
        if parent_node == self._root_node:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.row, 0, parent_node)

    def index(self, row, column, parent):
        if not parent.isValid():
            parent_node = self._root_node
        else:
            parent_node = parent.internalPointer()
        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()


class ChanelEditDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        super(ChanelEditDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 1:
            line_edit = QtGui.QLineEdit(parent)
            return line_edit

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class PublishButtonDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        super(PublishButtonDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        pub_button = QtGui.QPushButton(parent)
        pub_button.setText("Publish")
        src_index = index.model().mapToSource(index)
        pub_button.node = src_index.internalPointer()
        if not self.parent().indexWidget(index):
            self.parent().setIndexWidget(index, pub_button)
        if not pub_button.node.publish_paths:
            pub_button.setEnabled(False)
        pub_button.clicked.connect(self.do_publish)
        return pub_button

    def do_publish(self):
        # todo: publish single file here
        node = self.sender().node
        print '''
        texture %s
        pub path %s''' % (node.name, node.publish_paths)


def run_maya():
    wgt = TexturePublishToolGUI(getMayaWindow())
    wgt.show()


if __name__ == "__main__":
    pass
