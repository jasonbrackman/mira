# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import loader_ui
reload(loader_ui)
import miraCore
from miraLibs.pipeLibs import pipeMira, get_current_project
from miraLibs.dbLibs import db_api
from miraLibs.qtLibs import create_round_rect_thumbnail
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import join_path, yml_operation


IMAGE_WIDTH = 100


class AssetItem(object):
    def __init__(self, project=None, typ=None, name=None, image_path=None):
        self.project = project
        self.typ = typ
        self.name = name
        self.image_path = image_path


class LoaderModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(LoaderModel, self).__init__(parent)
        self.model_data = model_data

    def rowCount(self, parent=QModelIndex()):
        return len(self.model_data)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        item = self.model_data[row]
        if role == Qt.DisplayRole:
            name = item.name
            elidfont = QFontMetrics(QFont("Arial", 12))
            text = elidfont.elidedText(name, Qt.ElideRight, IMAGE_WIDTH)
            return text
        if role == Qt.ToolTipRole:
            return item.name
        if role == Qt.DecorationRole:
            # image = create_round_rect_thumbnail.create_round_rect_thumbnail(item.image_path, IMAGE_WIDTH, IMAGE_WIDTH, 10)
            image = QPixmap(item.image_path)
            image = image.scaled(QSize(100, 100), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            return image
        # if role == Qt.ForegroundRole:
        #     if not self.model_data[row].publish_path:
        #         return QColor(255, 0, 0)
        #     else:
        #         return QColor(0, 255, 0)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for index, i in enumerate(value):
            self.model_data.insert(position+index, i)
        self.model_data.sort(key=lambda x: x.name)
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.model_data[position]
            self.model_data.remove(value)
        self.endRemoveRows()
        return True

    def setData(self, index, value, role):
        row = index.row()
        if value:
            if role == Qt.DecorationRole:
                self.model_data[row] = value
                self.dataChanged.emit(index, index)
            return True

    def remove_all(self):
        for i in xrange(self.rowCount()):
            self.removeRows(0, 1)


class Loader(loader_ui.LoaderUI):
    def __init__(self, parent=None):
        super(Loader, self).__init__(parent)
        self.init_project()
        self.init_asset_type()
        self.set_signals()
        self.__db = db_api.DbApi(self.project).db_obj
        self.__image_dir = miraCore.get_icons_dir()

    @property
    def project(self):
        return self.project_cbox.currentText()

    @property
    def asset_type(self):
        return self.asset_btn_grp.checkedButton().text()

    def init_project(self):
        projects = pipeMira.get_projects()
        current_project = get_current_project.get_current_project()
        self.project_cbox.addItems(projects)
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(current_project))

    def init_asset_type(self):
        asset_types = pipeMira.get_studio_value(self.project, "asset_type")
        for asset_type in asset_types:
            self.asset_type_check = QCheckBox(asset_type)
            self.asset_btn_grp.addButton(self.asset_type_check)
            self.asset_layout.addWidget(self.asset_type_check)

    def set_signals(self):
        self.asset_btn_grp.buttonClicked[QAbstractButton].connect(self.show_assets)

    def set_model(self, model_data):
        self.asset_proxy_model = QSortFilterProxyModel()
        self.asset_proxy_model.setDynamicSortFilter(True)
        self.asset_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_le.textChanged.connect(self.asset_proxy_model.setFilterRegExp)
        self.asset_model = LoaderModel(model_data)
        self.asset_proxy_model.setSourceModel(self.asset_model)
        self.list_view.setModel(self.asset_proxy_model)

    def show_assets(self, btn):
        import time
        start = time.time()
        project = self.project
        asset_type = btn.text()
        assets = self.__db.get_all_assets(asset_type)
        if not assets:
            return
        model_data = list()
        studio_conf_path = join_path.join_path2(miraCore.get_conf_dir(), "studio.yml")
        yml_data = yml_operation.get_yaml_data(studio_conf_path)
        project_data = yml_data.get(self.project)
        primary = project_data.get("primary")
        format_str = project_data.get("maya_asset_image")
        print time.time()-start
        print format_str
        start = time.time()
        for asset in assets:
            asset_name = asset.get("name")
            image_path = format_str.format(primary=primary, project=project, asset_type=asset_type,
                                           asset_name=asset_name, step="MidMdl", task="MidMdl", engine="maya")
            if not os.path.isfile(image_path):
                image_path = join_path.join_path2(self.__image_dir, "unknown.png")
            item = AssetItem(project, asset_type, asset_name, image_path)
            model_data.append(item)
        print time.time()-start
        start = time.time()
        self.set_model(model_data)
        print time.time()-start


if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(Loader)
