# -*- coding: utf-8 -*-
import os
import shutil
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import maya.mel as mel
from miraLibs.pyLibs import get_range_data
from miraLibs.mayaLibs import get_maya_win


class RenderLayer(object):
    def __init__(self, name=None, camera=None, frames=None):
        self.name = name
        self.camera = camera
        self.frames = frames
        self.renderable = None
        self.model = "Maya"


class Maya(object):
    @staticmethod
    def render(layer, camera, frame):
        mc.RenderViewWindow()
        # for layer in layers:
        mc.editRenderLayerGlobals(currentRenderLayer=layer)
        mc.currentTime(frame)
        mel.eval('renderWindowRenderCamera render renderView ' + camera)

    @staticmethod
    def get_render_layers():
        render_layers = mc.ls(type='renderLayer')
        render_layers = [layer for layer in render_layers if 'defaultRenderLayer' not in layer]
        return render_layers

    @staticmethod
    def get_camera():
        cameras = mc.ls(cameras=1)
        return cameras

    @staticmethod
    def get_default_render_camera():
        render_camera = [cam for cam in mc.ls(cameras=1) if mc.getAttr("%s.renderable" % cam)]
        return render_camera

    @staticmethod
    def get_renderable(renderlayer):
        return mc.getAttr("%s.renderable" % renderlayer)

    @staticmethod
    def get_default_frame_range():
        first = mc.getAttr("defaultRenderGlobals.startFrame")
        end = mc.getAttr("defaultRenderGlobals.endFrame")
        return "%s-%s" % (int(first), int(end))

    @staticmethod
    def set_current_render_layer(renderlayer):
        mc.editRenderLayerGlobals(crl=renderlayer)

    @staticmethod
    def set_render_frame_ext():
        mc.setAttr("defaultRenderGlobals.outFormatControl", 0)
        mc.setAttr("defaultRenderGlobals.animation", 1)
        mc.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
        mc.setAttr("defaultRenderGlobals.extensionPadding", 4)
        mc.setAttr("defaultRenderGlobals.periodInExt", 1)

    @staticmethod
    def get_current_render_frame_path(current_frame):
        fist_image = mc.renderSettings(fin=1, fp=1)[0]
        fist_image_list = fist_image.split(".")
        prefix = ".".join(fist_image_list[:-2])
        frame = str(current_frame).zfill(4)
        ext = fist_image_list[-1]
        current_frame_path = ".".join([prefix, frame, ext])
        return current_frame_path

    @staticmethod
    def copy_from_temp(frame_path):
        frame_dir = os.path.dirname(frame_path)
        if not os.path.isdir(frame_dir):
            os.makedirs(frame_dir)
        if os.path.isfile(frame_path):
            os.remove(frame_path)
        prefix, suffix = frame_path.split("images")
        temp_path = "%simages/tmp%s" % (prefix, suffix)
        shutil.copyfile(temp_path, frame_path)


class SetFrameWidget(QWidget):
    def __init__(self, parent=None):
        super(SetFrameWidget, self).__init__(parent)
        self.maya = Maya()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)
        check_layout = QHBoxLayout()
        self.maya_check = QCheckBox("Maya")
        self.custom_check = QCheckBox("Custom")
        for check in [self.maya_check, self.custom_check]:
            check_layout.addWidget(check)
            self.btn_group.addButton(check)
        self.frame_te = QTextEdit()
        main_layout.addLayout(check_layout)
        main_layout.addWidget(self.frame_te)
        self.init()
        self.set_signals()

    def init(self):
        self.maya_check.setChecked(True)
        self.frame_te.setEnabled(False)

    def set_signals(self):
        self.btn_group.buttonClicked.connect(self.set_frame_status)

    def set_frame_status(self, btn):
        if btn is self.maya_check:
            self.frame_te.setText(self.maya.get_default_frame_range())
            self.frame_te.setEnabled(False)
        else:
            self.frame_te.setEnabled(True)

    def set_frame(self, value):
        self.frame_te.setText(value)


class RenderModel(QAbstractTableModel):
    def __init__(self, arg=[], header=[], parent=None):
        super(RenderModel, self).__init__(parent)
        self.arg = arg
        self.header = header

    def rowCount(self, parent=QModelIndex()):
        return len(self.arg)

    def columnCount(self, parent=QModelIndex()):
        return 6

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.arg[row][column]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.arg[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]


class RenderDelegate(QItemDelegate):
    mandatory_signal = Signal(list)
    camera_signal = Signal(list)
    frame_signal = Signal(list)
    model_signal = Signal(list)

    def __init__(self, parent=None):
        super(RenderDelegate, self).__init__(parent)
        self.maya = Maya()

    def createEditor(self, parent, option, index):
        if index.column() == 0:
            editor = QCheckBox(parent)
            editor.index = index
            editor.stateChanged.connect(self.emit_mandatory_signal)
        elif index.column() == 2:
            editor = QComboBox(parent)
            editor.index = index
            cameras = self.maya.get_camera()
            editor.addItems(cameras)
            camera = self.maya.get_default_render_camera()[0]
            editor.setCurrentIndex(editor.findText(camera))
            editor.currentIndexChanged[unicode].connect(self.emit_camera_signal)
        elif index.column() == 3:
            editor = SetFrameWidget(parent)
            editor.frame_te.index = index
            editor.btn_group.index = index
            editor.frame_te.textChanged.connect(self.emit_frame_signal)
            editor.btn_group.buttonClicked.connect(self.emit_model_signal)
        return editor

    def setEditorData(self, editor, index):
        render_item_index = index.model().index(index.row(), 5)
        render_item = render_item_index.data()
        if index.column() == 0:
            value = render_item.renderable
            editor.setChecked(value)
        elif index.column() == 3:
            frames = render_item.frames
            editor.set_frame(frames)

    def setModelData(self, editor, model, index):
        if index.column() == 2:
            value = editor.currentText()
            model.setData(index, value)
        elif index.column() == 3:
            value = editor.frames
            model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def emit_camera_signal(self, text):
        self.commitData.emit(self.sender())
        self.camera_signal.emit([self.sender().index, text])

    def emit_mandatory_signal(self, state):
        self.mandatory_signal.emit([self.sender().index, state])

    def emit_frame_signal(self):
        text = self.sender().toPlainText()
        self.frame_signal.emit([self.sender().index, text])

    def emit_model_signal(self):
        btn = self.sender().checkedButton()
        self.model_signal.emit([self.sender().index, btn])


class ForegroundRender(QDialog):
    def __init__(self, parent=None):
        super(ForegroundRender, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.resize(600, 300)
        self.setWindowTitle("ForegroundRender")
        self.maya = Maya()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 3)
        self.table_view = QTableView()
        self.table_view.verticalHeader().hide()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.NoSelection)
        btn_layout = QHBoxLayout()
        self.tip_label = QLabel()
        self.tip_label.setText(u'<font color="#FF9c20">[Tip]: frame设置格式：1-20,25,30,35-40</font>')
        self.tip_label.setAlignment(Qt.AlignLeft)
        self.render_btn = QPushButton("Render")
        self.shut_down_check = QCheckBox("shutdown after render completed.")
        self.shut_down_check.setChecked(False)
        btn_layout.addWidget(self.tip_label)
        btn_layout.addStretch()
        btn_layout.addWidget(self.shut_down_check)
        btn_layout.addWidget(self.render_btn)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(btn_layout)
        self.set_model()
        self.set_delegate()
        self.set_progress_bar()
        self.set_signals()

    def set_model(self):
        headers = ["renderable", "renderlayer", "camera", "frames", "progress", ""]
        model_data = list()
        render_layers = self.maya.get_render_layers()
        default_render_camera = self.maya.get_default_render_camera()
        frames = self.maya.get_default_frame_range()
        if render_layers:
            for render_layer in render_layers:
                item = RenderLayer()
                item.renderable = self.maya.get_renderable(render_layer)
                item.name = render_layer
                item.camera = default_render_camera[0]
                item.frames = frames
                model_data.append(["", item.name, item.camera, item.frames, "", item])
        self.data_model = RenderModel(model_data, headers)
        self.table_view.setModel(self.data_model)
        self.table_view.resizeColumnToContents(1)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.hideColumn(5)
        self.table_view.setColumnWidth(3, 150)
        for i in xrange(self.data_model.rowCount()):
            self.table_view.setRowHeight(i, 60)

    def set_delegate(self):
        delegate = RenderDelegate(self)
        delegate.mandatory_signal.connect(self.set_mandatory)
        delegate.camera_signal.connect(self.set_camera)
        delegate.frame_signal.connect(self.set_frame)
        delegate.model_signal.connect(self.set_run_model)
        self.table_view.setItemDelegate(delegate)
        self.show_delegate()

    def show_delegate(self):
        for i in xrange(self.data_model.rowCount()):
            self.table_view.openPersistentEditor(self.data_model.index(i, 0))
            self.table_view.openPersistentEditor(self.data_model.index(i, 2))
            self.table_view.openPersistentEditor(self.data_model.index(i, 3))

    def set_progress_bar(self):
        for i in xrange(self.data_model.rowCount()):
            progress_bar = QProgressBar()
            self.table_view.setIndexWidget(self.data_model.index(i, 4), progress_bar)

    def set_signals(self):
        self.render_btn.clicked.connect(self.do_render)

    def set_mandatory(self, index_and_value):
        item_index = self.data_model.index(index_and_value[0].row(), 5)
        render_item = item_index.data()
        render_item.renderable = index_and_value[1]

    def set_camera(self, index_and_value):
        item_index = self.data_model.index(index_and_value[0].row(), 5)
        render_item = item_index.data()
        render_item.camera = index_and_value[1]

    def set_frame(self, index_and_value):
        item_index = self.data_model.index(index_and_value[0].row(), 5)
        render_item = item_index.data()
        render_item.frames = index_and_value[1]

    def set_run_model(self, index_and_value):
        item_index = self.data_model.index(index_and_value[0].row(), 5)
        render_item = item_index.data()
        render_item.model = index_and_value[1].text()

    def do_render(self):
        self.maya.set_render_frame_ext()
        row_count = self.data_model.rowCount()
        mc.progressWindow(title="Rendering...",
                          isInterruptable=1,
                          status="start rendering...",
                          min=0, max=row_count,
                          progress=0)
        for row in xrange(row_count):
            item_index = self.data_model.index(row, 5)
            render_item = item_index.data()
            progress_bar = self.table_view.indexWidget(self.data_model.index(row, 4))
            render_layer = render_item.name
            render_model = render_item.model
            if render_item.renderable:
                mc.editRenderLayerGlobals(currentRenderLayer=render_layer)
                camera = render_item.camera
                if render_model == "Custom":
                    frames = get_range_data.get_range_data(render_item.frames)
                else:
                    frame_range = self.maya.get_default_frame_range()
                    frames = get_range_data.get_range_data(frame_range)
                progress_bar.setRange(0, len(frames))
                for frame_index, frame in enumerate(frames):
                    if mc.progressWindow(query=1, isCancelled=1):
                        print "Interrupt by press Esc."
                        break
                    mc.RenderViewWindow()
                    mel.eval("setTestResolutionVar(1)")
                    mc.currentTime(frame)
                    current_frame_render_path = self.maya.get_current_render_frame_path(frame)
                    mel.eval('renderWindowRenderCamera render renderView ' + camera)
                    self.maya.copy_from_temp(current_frame_render_path)
                    print "render to %s" % current_frame_render_path
                    progress_bar.setValue(frame_index+1)
        mc.progressWindow(endProgress=1)
        if self.shut_down_check.isChecked():
            os.system("shutdown -s -t 60")


def main():
    mc.editRenderLayerGlobals(crl="defaultRenderLayer")
    sfw = ForegroundRender(get_maya_win.get_maya_win("PySide"))
    sfw.show()


if __name__ == "__main__":
    main()
