# -*- coding: utf-8 -*-
import os
import logging
from PySide import QtGui, QtCore
import add_environ
from asset_library_libs.screen_shot.screen_shot import ThumbnailWidget
from asset_library_libs.get_conf_data import get_conf_data
from asset_library_libs.get_engine import get_engine
from asset_library_libs.start_file import start_file
from asset_library_libs.export_abc import AbcExporter
from asset_library_libs.export_texture import TexExporter
from asset_library_libs.export_shd import ShdExporter


logger = logging.getLogger("Asset library output")


class ComboModel(QtCore.QAbstractListModel):
    def __init__(self, model_data=None, parent=None):
        super(ComboModel, self).__init__(parent)
        self.model_data = model_data
        self.parent = parent

    def rowCount(self, parent):
        return len(self.model_data)+1

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        row = index.row()
        if row < len(self.model_data):
            if role == QtCore.Qt.DisplayRole:
                return self.model_data[row]
            elif role == QtCore.Qt.SizeHintRole:
                return QtCore.QSize(self.parent.width(), 25)

    def setData(self, index, value, role):
        row = index.row()
        if value:
            if role == QtCore.Qt.DisplayRole:
                self.model_data[row] = value
                self.dataChanged.emit(index, index)
            return True

    def insertRows(self, position, count, value, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for index, i in enumerate(value):
            self.model_data.insert(position+index, i)
        self.endInsertRows()
        return True


class Output(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Output, self).__init__(parent)
        self.engine = get_engine()
        self.conf_data = get_conf_data()
        self.asset_library_dir = self.conf_data["asset_library_dir"].format(engine=self.engine)
        self.category_list = list()
        self.setup_ui()
        self.init()
        self.set_signals()

    def setup_ui(self):
        self.resize(400, 500)
        main_layout = QtGui.QVBoxLayout(self)

        category_layout = QtGui.QHBoxLayout()
        category_label = QtGui.QLabel("Category")
        category_label.setFixedWidth(50)
        self.category_cbox = QtGui.QComboBox()
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_cbox)

        name_layout = QtGui.QHBoxLayout()
        name_label = QtGui.QLabel("Name")
        name_label.setFixedWidth(50)
        name_label.setAlignment(QtCore.Qt.AlignRight)
        self.name_le = QtGui.QLineEdit()
        self.name_le.setPlaceholderText("Please input an asset name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_le)

        screen_layout = QtGui.QHBoxLayout()
        screen_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.screen_widget = ThumbnailWidget()
        self.screen_widget.setFixedSize(380, 380)
        screen_layout.addWidget(self.screen_widget)

        path_layout = QtGui.QGridLayout()
        mdl_path__label = QtGui.QLabel("mdl path")
        self.mdl_path_le = QtGui.QLineEdit()
        tex_dir_label = QtGui.QLabel("tex dir")
        self.tex_dir_le = QtGui.QLineEdit()
        shd_path_label = QtGui.QLabel("shd path")
        self.shd_path_le = QtGui.QLineEdit()
        pic_path_label = QtGui.QLabel("pic path")
        self.pic_path_le = QtGui.QLineEdit()
        for le in [self.mdl_path_le, self.tex_dir_le, self.shd_path_le, self.pic_path_le]:
            le.setReadOnly(True)
        path_layout.addWidget(mdl_path__label, 0, 0)
        path_layout.addWidget(self.mdl_path_le, 0, 1)
        path_layout.addWidget(tex_dir_label, 1, 0)
        path_layout.addWidget(self.tex_dir_le, 1, 1)
        path_layout.addWidget(shd_path_label, 2, 0)
        path_layout.addWidget(self.shd_path_le, 2, 1)
        path_layout.addWidget(pic_path_label, 3, 0)
        path_layout.addWidget(self.pic_path_le, 3, 1)

        self.submit_btn = QtGui.QPushButton("Submit")
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setTextVisible(False)

        main_layout.addLayout(category_layout)
        main_layout.addLayout(name_layout)
        main_layout.addLayout(screen_layout)
        main_layout.addLayout(path_layout)
        main_layout.addWidget(self.submit_btn)
        main_layout.addWidget(self.progress_bar)

    def init(self):
        self.set_combo_view()
        self.show_path()

    def set_signals(self):
        self.submit_btn.clicked.connect(self.do_submit)
        self.category_cbox.currentIndexChanged.connect(self.show_path)
        self.name_le.textChanged.connect(self.show_path)

    def set_combo_view(self):
        if os.path.isdir(self.asset_library_dir):
            self.category_list = os.listdir(self.asset_library_dir)
        self.category_model = ComboModel(self.category_list, self.category_cbox)
        self.category_cbox.setModel(self.category_model)
        self.category_view = self.category_cbox.view()
        self.add_category_btn = QtGui.QPushButton("Add category")
        self.add_category_btn.clicked.connect(self.add_category)
        btn_index = self.category_model.index(len(self.category_list))
        self.category_view.setIndexWidget(btn_index, self.add_category_btn)

    def add_category(self):
        inputs = QtGui.QInputDialog.getText(self, "Input a category name", "category name:")
        if inputs[1]:
            text = inputs[0]
            self.category_model.insertRows(0, 1, [text])
            self.category_cbox.setCurrentIndex(0)

    def show_path(self):
        category = str(self.category_cbox.currentText())
        name = str(self.name_le.text())
        mdl_path = self.conf_data[self.engine]["mdl_path"].format(engine=self.engine, category=category, name=name)
        tex_dir = self.conf_data[self.engine]["tex_dir"].format(engine=self.engine, category=category, name=name)
        shd_path = self.conf_data[self.engine]["shd_path"].format(engine=self.engine, category=category, name=name)
        pic_path = self.conf_data[self.engine]["pic_path"].format(engine=self.engine, category=category, name=name)
        self.mdl_path_le.setText(mdl_path)
        self.tex_dir_le.setText(tex_dir)
        self.shd_path_le.setText(shd_path)
        self.pic_path_le.setText(pic_path)

    @property
    def pixmap(self):
        return self.screen_widget._get_thumbnail()

    def submit_mdl(self):
        mdl_path = str(self.mdl_path_le.text())
        ep = AbcExporter(mdl_path)
        ep.export()

    def submit_picture(self):
        pic_path = str(self.pic_path_le.text())
        if self.pixmap:
            self.pixmap.save(pic_path)

    def submit_tex(self):
        tex_dir = str(self.tex_dir_le.text())
        tp = TexExporter(tex_dir)
        tp.export()

    def submit_shd(self):
        shd_path = str(self.shd_path_le.text())
        tex_dir = str(self.tex_dir_le.text())
        se = ShdExporter(shd_path, tex_dir)
        se.export()

    def do_submit(self):
        if not self.pixmap:
            QtGui.QMessageBox.warning(None, "Warning", "Screen shot first please.")
            return
        category = str(self.category_cbox.currentText())
        name = str(self.name_le.text())
        if not all((category, name)):
            QtGui.QMessageBox.warning(self, "warning", "Make sure category and name is right.")
            return
        asset_dir = os.path.join(self.asset_library_dir, category, name).replace("\\", "/")
        if os.path.isdir(asset_dir):
            message_box = QtGui.QMessageBox.warning(self, "warning",
                                                    "%s is an exist directory, Do you want to replace it?" % asset_dir,
                                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
            if message_box.name == "Cancel":
                return
        self.progress_bar.setRange(0, 4)
        self.progress_bar.setValue(0)
        self.submit_mdl()
        logger.info("Submit mdl done.")
        self.progress_bar.setValue(1)
        self.submit_picture()
        logger.info("Submit picture done.")
        self.progress_bar.setValue(2)
        self.submit_tex()
        logger.info("Submit texture done.")
        self.progress_bar.setValue(3)
        self.submit_shd()
        logger.info("Submit shd done.")
        self.progress_bar.setValue(4)
        start_file(asset_dir)


def main():
    op = Output()
    op.show()


if __name__ == "__main__":
    main()
