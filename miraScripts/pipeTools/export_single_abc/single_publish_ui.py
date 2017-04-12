# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
from miraFramework.Filter import ButtonLineEdit
from miraLibs.pyLibs import join_path
import miraCore


class SinglePublishUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(SinglePublishUI, self).__init__(parent)
        self.resize(400, 300)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 1, 0, 1)
        # filter layout
        filter_layout = QtGui.QHBoxLayout()
        filter_layout.addStretch()
        self.filter_le = ButtonLineEdit()
        filter_layout.addWidget(self.filter_le)
        self.update_btn = QtGui.QToolButton()
        icon_path = join_path.join_path2(miraCore.get_icons_dir(), "update.png")
        self.update_btn.setIcon(QtGui.QIcon(icon_path))
        self.update_btn.setStyleSheet("QToolButton{background:transparent;}"
                                      "QToolButton::hover{background:#00BFFF;border-color:#00BFFF;}")
        filter_layout.addWidget(self.update_btn)
        # table view
        self.table_view = QtGui.QTableView()
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table_view)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    sp = SinglePublishUI()
    sp.show()
    app.exec_()

