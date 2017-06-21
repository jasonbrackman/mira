# -*- coding: utf-8 -*-
import logging
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
import set_duration
import reset_dialog
reload(reset_dialog)         # reload UI file

Settings = QSettings("OddOrange", "MayaSaveTimer")


class ResetUI(QDialog):

    def __init__(self, parent=None):
        super(ResetUI, self).__init__(parent)

        self._ui = reset_dialog.Ui_reset_dlg()
        self._ui.setupUi(self)

        # get current setting
        duration_value = Settings.value("duration")
        if not duration_value:
            duration = 20
        else:
            duration = duration_value
        # set default
        self._ui.duration_spin.setValue(duration)

    @Slot()
    def on_ok_btn_clicked(self):
        duration = int(self._ui.duration_spin.text())
        logging.debug("new duration is %s minutes." % duration)
        set_duration.set_duration(duration)


if __name__ == "__main__":
    pass
