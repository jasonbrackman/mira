# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from miraFramework.Filter import Filter
import miraCore
from miraLibs.pyLibs import join_path


class ReplaceAssetUI(QDialog):
    def __init__(self, parent=None):
        super(ReplaceAssetUI, self).__init__(parent)
        self.resize(1000, 600)
        self.setObjectName("Replace Asset")
        self.setup_ui()
        self.setWindowFlags(Qt.Window)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 2, 0, 0)
        top_layout = QHBoxLayout()

        convert_layout = QHBoxLayout()
        convert_label = QLabel("Convert")
        self.src_cbox = QComboBox()
        to_label = QLabel("=========>")
        self.dst_cbox = QComboBox()
        convert_layout.addWidget(convert_label)
        convert_layout.addWidget(self.src_cbox)
        convert_layout.addWidget(to_label)
        convert_layout.addWidget(self.dst_cbox)

        self.select_check = QCheckBox("Select in Maya")
        self.select_check.setChecked(True)

        self.filter_le = Filter()
        self.filter_le.setPlaceholderText("Search...")
        self.update_btn = QToolButton()
        icon_path = join_path.join_path2(miraCore.get_icons_dir(), "update.png")
        self.update_btn.setIcon(QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;border: 0px;}"
                                      "QToolButton::hover{background:#AAAAAA;}")

        top_layout.addLayout(convert_layout)
        top_layout.addWidget(self.select_check)
        top_layout.addStretch()
        top_layout.addWidget(self.filter_le)
        top_layout.addWidget(self.update_btn)

        self.tree_view = QTreeView()

        btn_layout = QHBoxLayout()
        self.replace_btn = QPushButton("Replace")
        self.replace_btn.setFixedHeight(30)
        btn_layout.addWidget(self.replace_btn)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tree_view)
        main_layout.addLayout(btn_layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    rau = ReplaceAssetUI()
    rau.show()
    app.exec_()




