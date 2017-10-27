# -*- coding: utf-8 -*-
import os
import functools
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import layout_producer_ui
reload(layout_producer_ui)
import pipeGlobal
from miraLibs.pipeLibs import pipeMira, pipeFile
from miraLibs.pyLibs import join_path, get_latest_version_by_dir
from miraLibs.mayaLibs import create_reference, import_gpu_cache, add_string_attr, show_as_panel
from miraLibs.pipeLibs.pipeMaya import get_current_project


qss_path = join_path.join_path2(os.path.dirname(__file__), "style.qss")


class ListModelItem(object):
    def __init__(self, name=None, image_path=None, publish_path=None):
        self.name = name
        self.image_path = image_path
        self.publish_path = publish_path


class ListModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__model_data = model_data

    @property
    def model_data(self):
        return self.__model_data

    @model_data.setter
    def model_data(self, value):
        self.__model_data = value

    def rowCount(self, parent=QModelIndex()):
        return len(self.__model_data)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if role == Qt.DisplayRole:
            return self.__model_data[row].name
        if role == Qt.ToolTipRole:
            publish_path = self.__model_data[row].publish_path
            if publish_path:
                obj = pipeFile.PathDetails.parse_path(publish_path)
                context_version = obj.context_version
                version = obj.current_version_str
                if context_version:
                    return "%s\n%s" % (context_version, version)
                else:
                    return version
        if role == Qt.DecorationRole:
            pix_map_path = self.__model_data[row].image_path
            icon_dir = pipeGlobal.icons_dir
            if not pix_map_path:
                pix_map_path = join_path.join_path2(icon_dir, "unknown.png")
            pix_map = QPixmap(pix_map_path)
            scaled = pix_map.scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scaled.setMask(QBitmap(join_path.join_path2(icon_dir, "round_corner_mask.png")))
            return scaled
        if role == Qt.ForegroundRole:
            if not self.__model_data[row].publish_path:
                return QColor(255, 0, 0)
            else:
                return QColor(0, 255, 0)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for index, i in enumerate(value):
            self.__model_data.insert(position+index, i)
        self.__model_data.sort(key=lambda x: x.name)
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.__model_data[position]
            self.__model_data.remove(value)
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


class CollectAssetsThread(QThread):
    signal = Signal(list)

    def __init__(self, asset_type_dir=None, low=True, parent=None):
        super(CollectAssetsThread, self).__init__(parent)
        self.__asset_type_dir = asset_type_dir
        self.low = low

    @property
    def asset_type_dir(self):
        return self.__asset_type_dir

    @asset_type_dir.setter
    def asset_type_dir(self, value):
        self.__asset_type_dir = value

    def run(self):
        asset_type = os.path.basename(self.__asset_type_dir)
        asset_names = [i for i in os.listdir(self.__asset_type_dir)
                       if os.path.isdir(join_path.join_path2(self.__asset_type_dir, i)) and not i.startswith(".")]
        if not asset_names:
            self.signal.emit([])
            return
        for asset_name in asset_names:
            image_path = None
            publish_path = None
            if asset_type in ["Environment"]:
                category = "lowMld" if self.low else "mdl"
                asset_image_dir = join_path.join_path2(self.__asset_type_dir, asset_name, category, "_image")
                asset_publish_dir = join_path.join_path2(self.__asset_type_dir, asset_name, category, "_publish")
                latest_image = get_latest_version_by_dir.get_latest_version_by_dir(asset_image_dir)
                latest_publish = get_latest_version_by_dir.get_latest_version_by_dir(asset_publish_dir)
                if latest_image:
                    image_path = latest_image[0]
                if latest_publish:
                    publish_path = latest_publish[0]
                self.signal.emit([asset_name, image_path, publish_path])
            else:
                category = "lowRig" if self.low else "rig"
                rig_folder = join_path.join_path2(self.__asset_type_dir, asset_name, category)
                if os.path.isdir(rig_folder):
                    for folder in os.listdir(rig_folder):
                        asset_image_dir = join_path.join_path2(rig_folder, folder, "_image")
                        asset_publish_dir = join_path.join_path2(rig_folder, folder, "_publish")
                        latest_image = get_latest_version_by_dir.get_latest_version_by_dir(asset_image_dir)
                        if latest_image:
                            image_path = latest_image[0]
                        latest_publish = get_latest_version_by_dir.get_latest_version_by_dir(asset_publish_dir)
                        if latest_publish:
                            publish_path = latest_publish[0]
                        self.signal.emit([asset_name, image_path, publish_path])
                else:
                    self.signal.emit([asset_name, image_path, publish_path])


class LayoutProducer(layout_producer_ui.LayoutProducerUI):
    def __init__(self, parent=None):
        super(LayoutProducer, self).__init__(parent)
        self.setObjectName("LayoutProducer")
        self.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet(open(qss_path, 'r').read())
        self.setWindowFlags(Qt.Window)
        self.__threads = list()
        self.__show_thread = CollectAssetsThread()
        self.__projects = pipeMira.get_projects()
        self.__current_project = get_current_project.get_current_project()
        self.__asset_model_data = list()
        self.__include_model_data = list()
        self.init()
        self.set_asset_model()
        self.set_include_model()
        self.set_signals()

    def init(self):
        self.project_cbox.addItems(self.__projects)
        self.project_cbox.setCurrentIndex(self.project_cbox.findText(self.__current_project))
        self.name_space_cbox.addItems(["asset name", "no namespace"])

    def set_signals(self):
        self.asset_btn_grp.buttonClicked.connect(self.show_asset_icons)
        self.low_check.stateChanged.connect(self.show_asset_icons)
        self.add_btn.clicked.connect(self.add_to_include)
        self.reference_all_btn.clicked.connect(functools.partial(self.reference, True))
        self.reference_sel_btn.clicked.connect(functools.partial(self.reference, False))
        self.__show_thread.signal.connect(self.collect_assets)
        self.update_btn.clicked.connect(self.show_asset_icons)
        self.project_cbox.currentIndexChanged.connect(self.on_change_project)
        self.asset_list_view.launch_action.triggered.connect(self.launch_folder)
        self.include_list_view.launch_action.triggered.connect(self.launch_folder)
        self.asset_list_view.doubleClicked.connect(self.do_create_reference)

    def do_create_reference(self, index):
        index = self.asset_list_view.model().mapToSource(index)
        item = self.asset_model.model_data[index.row()]
        publish_path = item.publish_path
        namespace = item.name if self.name_space_cbox.currentText() == "asset name" else ":"
        if os.path.isfile(publish_path):
            create_reference.create_reference(publish_path, namespace, True)

    def set_asset_model(self):
        self.asset_proxy_model = QSortFilterProxyModel()
        self.asset_proxy_model.setDynamicSortFilter(True)
        self.asset_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_le.textChanged.connect(self.asset_proxy_model.setFilterRegExp)
        self.asset_model = ListModel(self.__asset_model_data)
        self.asset_proxy_model.setSourceModel(self.asset_model)
        self.asset_list_view.setModel(self.asset_proxy_model)

    def set_include_model(self):
        self.include_model = ListModel(self.__include_model_data)
        self.include_list_view.setModel(self.include_model)

    def show_asset_icons(self):
        self.__asset_model_data = list()
        current_project = self.project_cbox.currentText()
        root_dir = pipeMira.get_root_dir(current_project)
        button_text = self.asset_btn_grp.checkedButton().text()
        asset_type_dir = join_path.join_path2(root_dir, current_project, "assets", button_text)
        if not os.path.isdir(asset_type_dir):
            self.set_asset_model()
            return
        self.asset_model.remove_all()
        self.__show_thread.asset_type_dir = asset_type_dir
        self.__show_thread.low = self.low_check.isChecked()
        self.__show_thread.start()
        self.__threads.append(self.__show_thread)

    def collect_assets(self, value):
        if not value:
            self.__asset_model_data = list()
            self.set_asset_model()
            return
        item = ListModelItem(*value)
        self.asset_model.insertRows(self.asset_model.rowCount(), 1, [item])

    @staticmethod
    def get_list_view_items(list_view, get_all=False):
        if get_all:
            return list_view.get_model_data()
        else:
            selected_indexes = list_view.selectedIndexes()
            if not selected_indexes:
                return []
            selected = list()
            model = list_view.model()
            if isinstance(model, QSortFilterProxyModel):
                selected_rows = list(set([model.mapToSource(i).row() for i in selected_indexes]))
                for row in selected_rows:
                    data = model.sourceModel().model_data[row]
                    selected.append(data)
            else:
                selected = [model.model_data[i.row()] for i in selected_indexes]
            return selected

    @staticmethod
    def clear_list_view(list_view):
        model = list_view.model()
        if isinstance(model, QSortFilterProxyModel):
            model = model.sourceModel()
        model.remove_all()

    def on_change_project(self):
        self.__current_project = self.project_cbox.currentText()
        self.clear_list_view(self.asset_list_view)
        self.clear_list_view(self.include_list_view)
        checked_btn = self.asset_btn_grp.checkedButton()
        if not checked_btn:
            return
        self.asset_btn_grp.setExclusive(False)
        checked_btn.setChecked(False)
        self.asset_btn_grp.setExclusive(True)

    def add_to_include(self):
        selected_items = self.get_list_view_items(self.asset_list_view)
        if not selected_items:
            return
        self.include_model.insertRows(self.include_model.rowCount(), len(selected_items), selected_items)

    def launch_folder(self):
        selected_items = self.get_list_view_items(self.sender().parent())
        if not selected_items:
            return
        item = selected_items[0]
        publish_path = item.publish_path
        if publish_path and os.path.isfile(publish_path):
            os.startfile(os.path.dirname(publish_path))

    def reference(self, reference_all=False):
        items = self.get_list_view_items(self.include_list_view, reference_all)
        if not items:
            return
        reference_files = list()
        for item in items:
            publish_path = item.publish_path
            namespace = item.name if self.name_space_cbox.currentText() == "asset_name" else ":"
            reference_files.append([publish_path, namespace])
        # add progress dialog
        progress_dialog = QProgressDialog('Referencing...', 'Cancel', 0, len(reference_files))
        progress_dialog.setMinimumWidth(400)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()
        for index, reference_file in enumerate(reference_files):
            progress_dialog.setValue(index)
            if progress_dialog.wasCanceled():
                break
            reference_file_path, namespace = reference_file
            if not all((reference_file_path, namespace)):
                continue
            if reference_file_path.endswith(".abc"):
                self.import_env_gpu_cache(reference_file_path, namespace)
            else:
                create_reference.create_reference(reference_file_path, namespace, True, True)
        # put char in to char group, env to env group, prop to prop group
        self.organize_type_group()

    def organize_type_group(self):
        assets = list()
        for transform in mc.ls(assemblies=1):
            if transform.endswith("_ROOT") or transform.endswith("_MODEL"):
                assets.append(transform)
        if not assets:
            return
        for asset in assets:
            name = asset.split(":")[-1]
            if name.startswith("char"):
                self.organize_group(asset, "char")
            if name.startswith("env"):
                self.organize_group(asset, "env")
            if name.startswith("prop"):
                self.organize_group(asset, "prop")

    @staticmethod
    def organize_group(asset, group_name):
        if not mc.objExists(group_name):
            mc.select(clear=1)
            mc.group(empty=1, name=group_name)
        mc.parent(asset, group_name)

    def import_env_gpu_cache(self, reference_file_path, name):
        gpu_cache_name = "%sShape" % name
        parent_name = import_gpu_cache.import_gpu_cache(gpu_cache_name, name, reference_file_path)
        mdl_publish_path = pipeFile.get_asset_step_publish_file("environment", name, "mdl", self.__current_project)
        shd_publish_path = pipeFile.get_asset_step_publish_file("environment", name, "shd", self.__current_project)
        add_string_attr.add_string_attr(parent_name, "mdl_path", mdl_publish_path)
        add_string_attr.add_string_attr(parent_name, "shd_path", shd_publish_path)
        mc.setAttr("%s.rotatePivot" % parent_name, lock=1)
        mc.setAttr("%s.scalePivot" % parent_name, lock=1)


def main():
    lp = LayoutProducer()
    show_as_panel.show_as_panel(lp)


if __name__ == "__main__":
    main()
