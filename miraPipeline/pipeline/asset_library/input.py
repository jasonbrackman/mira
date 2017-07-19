# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import add_environ
from asset_library_libs.get_conf_data import get_conf_data
from asset_library_libs.get_engine import get_engine
from asset_library_frameworks.Filter import Filter
from asset_library_libs.get_icon_dir import get_icon_dir


class AssetItem(object):
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path


class ComboModel(QAbstractListModel):
    def __init__(self, model_data=None, parent=None):
        super(ComboModel, self).__init__(parent)
        self.model_data = model_data
        self.parent = parent

    def rowCount(self, parent):
        return len(self.model_data)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        row = index.row()
        if role == Qt.DisplayRole:
            return self.model_data[row]
        elif role == Qt.SizeHintRole:
            return QSize(self.parent.width(), 25)


class CellWidget(QWidget):
    def __init__(self, parent=None):
        super(CellWidget, self).__init__(parent)
        self.engine = get_engine()
        self.conf_data = get_conf_data()
        self.icon_dir = get_icon_dir()
        self.file_dir = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(160, 160)
        self.icon_label.setStyleSheet("QLabel{background: #000000;}")
        self.icon_label.setAlignment(Qt.AlignCenter)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        for option in self.conf_data[self.engine]["actions"]:
            btn = QToolButton(self)
            btn.name = option
            btn.setToolTip(option)
            icon = QIcon(os.path.join(self.icon_dir, "%s.png" % option))
            btn.setIcon(icon)
            btn.setFixedSize(20, 20)
            btn.setIconSize(QSize(18, 18))
            btn.clicked.connect(self.action)
            btn.setStyleSheet("QToolButton{background:transparent;border: 0px;}"
                              "QToolButton::hover{background:#00BFFF;}")
            btn_layout.addWidget(btn)
        btn_layout.setSpacing(0)
        btn_layout.setAlignment(Qt.AlignLeft)

        self.name_label = QLabel()
        self.name_label.setStyleSheet("background: transparent;")

        main_layout.addWidget(self.icon_label)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.name_label)

    def set_file_dir(self, value):
        self.file_dir = value
        self.show_in_view()

    def action(self):
        action_name = self.sender().name
        cmd_str = "from asset_library_libs.{engine}_actions import {name};reload({name});{name}.main(self.file_dir)"\
            .format(engine=self.engine, name=action_name)
        exec(cmd_str)

    def set_icon_label(self):
        name = os.path.basename(self.file_dir)
        icon_path = os.path.join(self.file_dir, "%s.png" % name)
        icon_path = icon_path.replace("\\", "/")
        pixmap = QPixmap(icon_path)
        label_width = self.icon_label.width()
        label_height = self.icon_label.height()
        image_width = pixmap.width()
        image_height = pixmap.height()
        if image_width > image_height:
            scaled = pixmap.scaled(QSize(label_width, image_width/label_width*image_height),
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            scaled = pixmap.scaled(QSize(label_height/label_height*image_width, label_height),
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(scaled)

    def set_name_label(self):
        base_name = os.path.basename(self.file_dir)
        elided_font = QFontMetrics(self.name_label.font())
        text = elided_font.elidedText(base_name, Qt.ElideMiddle, self.name_label.width())
        self.name_label.setText("<font size=4 color=#FFFFFF><b>%s</b></font>" % text)

    def show_in_view(self):
        self.set_icon_label()
        self.set_name_label()


class AssetDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(AssetDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        cell_widget = CellWidget(parent)
        return cell_widget

    def setEditorData(self, editor, index):
        item = index.model().data(index, Qt.DisplayRole)
        if item:
            editor.set_file_dir(item.path)

    def sizeHint(self, option, index):
        return QSize(160, 200)


class AssetModel(QAbstractListModel):
    def __init__(self, arg=[], parent=None):
        super(AssetModel, self).__init__(parent)
        self.arg = arg

    def rowCount(self, parent=QModelIndex()):
        return len(self.arg)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            return self.arg[row]

    def flags(self, index):
        return Qt.ItemIsEnabled


class AssetFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(AssetFilterProxyModel, self).__init__(parent)
        self.name_regexp = QRegExp()
        self.name_regexp.setCaseSensitivity(Qt.CaseInsensitive)
        self.name_regexp.setPatternSyntax(QRegExp.RegExp)

    def filterAcceptsRow(self, source_row, source_parent):
        name_index = self.sourceModel().index(source_row, 0, source_parent)
        item = self.sourceModel().data(name_index)
        if self.name_regexp.isEmpty():
            return True
        else:
            return self.name_regexp.exactMatch(item.name)

    def set_name_filter(self, regexp):
        regexp = ".*%s.*" % regexp if regexp else ""
        self.name_regexp.setPattern(regexp)
        self.invalidateFilter()


class Input(QWidget):
    def __init__(self, parent=None):
        super(Input, self).__init__(parent)
        self.engine = get_engine()
        self.conf_data = get_conf_data()
        self.asset_library_dir = self.conf_data["asset_library_dir"].format(engine=self.engine)
        self.setup_ui()
        self.init()
        self.set_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        category_layout = QHBoxLayout()
        category_label = QLabel("Category")
        category_label.setFixedWidth(50)
        self.category_cbox = QComboBox()
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_cbox)

        filter_layout = QHBoxLayout()
        self.filter_le = Filter()
        self.filter_le.setPlaceholderText("Search...")
        self.update_btn = QToolButton()
        icon_path = os.path.join(get_icon_dir(), "update.png").replace("\\", "/")
        self.update_btn.setIcon(QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;border: 0px;}"
                                      "QToolButton::hover{background:#757575;}")
        filter_layout.addStretch()
        filter_layout.addWidget(self.filter_le)
        filter_layout.addWidget(self.update_btn)

        self.list_view = QListView()
        self.list_view.setViewMode(QListView.IconMode)
        self.list_view.setResizeMode(QListView.Adjust)
        self.list_view.setFlow(QListView.LeftToRight)
        self.list_view.setMovement(QListView.Static)
        self.list_view.setFocusPolicy(Qt.NoFocus)
        self.list_view.setWrapping(True)
        self.list_view.setSpacing(15)

        main_layout.addLayout(category_layout)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.list_view)

    def init(self):
        if not os.path.isdir(self.asset_library_dir):
            return
        category_list = os.listdir(self.asset_library_dir)
        if not category_list:
            return
        category_model = ComboModel(category_list, self.category_cbox)
        self.category_cbox.setModel(category_model)
        self.category_cbox.setCurrentIndex(self.category_cbox.count()+1)

    def set_signals(self):
        self.category_cbox.currentIndexChanged.connect(self.refresh)
        self.update_btn.clicked.connect(self.refresh)

    def set_model(self):
        category = self.category_cbox.currentText()
        if not category:
            return
        category_dir = os.path.join(self.asset_library_dir, category).replace("\\", "/")
        asset_names = os.listdir(category_dir)
        if not asset_names:
            return
        model_data = [AssetItem(name, os.path.join(category_dir, name).replace("\\", "/"))
                      for name in asset_names]
        self.model = AssetModel(model_data)
        self.proxy_model = AssetFilterProxyModel(self)
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.model)
        self.filter_le.textChanged.connect(self.set_filter)
        self.list_view.setModel(self.proxy_model)
        return True

    def set_filter(self, value):
        self.proxy_model.set_name_filter(value)
        self.show_delegate()

    def set_delegate(self):
        delegate = AssetDelegate(self)
        self.list_view.setItemDelegate(delegate)
        self.show_delegate()

    def show_delegate(self):
        for i in xrange(self.proxy_model.rowCount()):
            self.list_view.openPersistentEditor(self.proxy_model.index(i, 0))

    def refresh(self):
        if self.set_model():
            self.set_delegate()
            self.show_delegate()
