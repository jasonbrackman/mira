from Qt.QtWidgets import *
from Qt.QtCore import *
from miraFramework.combo import CombBox
from miraFramework.combo.project_combo import ProjectCombo
from miraLibs.pipeLibs import pipeMira, pipeFile
from miraLibs.dbLibs import db_api
from miraLibs.pipeLibs.pipeMaya.hair import import_xgen_hair



class HairUI(QDialog):
    def __init__(self, parent=None):
        super(HairUI, self).__init__(parent)
        self.setWindowTitle("Import Hair")
        self.resize(300, 200)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)

        layout = QGridLayout()
        project_label = QLabel("Project")
        self.project_combo = ProjectCombo()
        asset_type_label = QLabel("Asset Type")
        self.asset_type_combo = CombBox()
        asset_name_label = QLabel("Asset Name")
        self.asset_name_le = QLineEdit()
        namespace_label = QLabel("namespace")
        self.namespace_le = QLineEdit()
        layout.addWidget(project_label, 0, 0, 1, 1)
        layout.addWidget(self.project_combo, 0, 1, 1, 3)
        layout.addWidget(asset_type_label, 1, 0, 1, 1)
        layout.addWidget(self.asset_type_combo, 1, 1, 1, 3)
        layout.addWidget(asset_name_label, 2, 0, 1, 1)
        layout.addWidget(self.asset_name_le, 2, 1, 1, 3)
        layout.addWidget(namespace_label, 3, 0, 1, 1)
        layout.addWidget(self.namespace_le, 3, 1, 1, 3)
        layout.setSpacing(20)
        self.import_btn = QPushButton("Import")

        main_layout.addLayout(layout)
        main_layout.addWidget(self.import_btn)

        self.__db = db_api.DbApi(self.project).db_obj

        self.init()
        self.set_signals()

    def init(self):
        asset_types = pipeMira.get_studio_value(self.project, "asset_type")
        self.asset_type_combo.addItems(asset_types)
        self.set_asset_name()

    def set_signals(self):
        self.asset_type_combo.currentIndexChanged.connect(self.set_asset_name)
        self.import_btn.clicked.connect(self.do_import)

    def set_asset_name(self):
        assets = self.__db.get_all_assets(self.asset_type)
        asset_names = [asset.get("name") for asset in assets]
        completer = QCompleter(asset_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.asset_name_le.setCompleter(completer)

    @property
    def project(self):
        return self.project_combo.currentText()

    @property
    def asset_type(self):
        return self.asset_type_combo.currentText()

    @property
    def asset_name(self):
        return self.asset_name_le.text()

    @property
    def namespace(self):
        return self.namespace_le.text()

    def do_import(self):
        publish_file = pipeFile.get_task_file(self.project, self.asset_type, self.asset_name,
                                              "Hair", "Hair", "maya_asset_publish", "")
        context = pipeFile.PathDetails.parse_path(publish_file)
        import_xgen_hair(context, str(self.namespace))


def main():
    from miraLibs.qtLibs import render_ui
    render_ui.render(HairUI)


if __name__ == "__main__":
    main()
