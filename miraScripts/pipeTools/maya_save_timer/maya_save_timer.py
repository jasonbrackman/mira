# -*- coding: utf-8 -*-
import PySide.QtCore as QtCore

import miraLibs.mayaLibs.MayaSaveTimer as MayaSaveTimer
import miraLibs.mayaLibs.get_maya_globals as get_maya_globals
import miraLibs.mayaLibs.get_maya_win as get_maya_win
import MainUI

Settings = QtCore.QSettings("OddOrange", "MayaSaveTimer")


def maya_save_timer():
    save_timer = MayaSaveTimer.MayaSaveTimer()
    maya_globals = get_maya_globals.get_maya_globals()
    maya_globals.add(save_timer=save_timer)

    # set default time
    duration_value = Settings.value("duration")
    if not duration_value:
        Settings.setValue("duration", 120)
        save_timer.duration = 120
    else:
        save_timer.duration = duration_value

    def _call_save_dialog():
        save_timer.stop()
        maya_ui = get_maya_win.get_maya_win("PySide")
        dlg = MainUI.MainUI(save_timer.duration, maya_ui)
        dlg.closed.connect(save_timer.start)
        dlg.show()

    save_timer.slot = _call_save_dialog
    save_timer.start()


if __name__ == "__main__":
    pass
