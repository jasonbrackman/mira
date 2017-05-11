#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_MainUI
# description : ''
# author      : Aaron Hui
# date        : 2015/12/31
# version     :
# usage       :
# notes       :

# Built-in modules
import logging
import os
# Third-party modules
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import pymel.core as pm

# Studio modules
import miraLibs.mayaLibs.aas_save_as as aas_save_as

# Local modules
import timer_dialog
reload(timer_dialog)         # reload UI file

logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_MainUI_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


class MainUI(QtGui.QDialog):
    closed = QtCore.Signal()

    def __init__(self, duration=20, parent=None):
        super(MainUI, self).__init__(parent)

        self._ui = timer_dialog.Ui_maya_save_timer_dlg()
        self._ui.setupUi(self)
        self.duration = duration
        self._ui.time_label.setText(str(self.duration))
        self._ui.time_label_1.setText(str(self.duration))

    @QtCore.Slot()
    def on_save_btn_clicked(self):
        logging.debug("default maya save.")
        pm.mel.eval("SaveScene")

    @QtCore.Slot()
    def on_versionup_btn_clicked(self):
        logging.debug("aas version up save.")
        aas_save_as.aas_save_as()

    def closeEvent(self, *args, **kwargs):
        logging.debug("close event")
        self.closed.emit()
        self.deleteLater()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    wgt = MainUI()
    wgt.show()
    app.exec_()
