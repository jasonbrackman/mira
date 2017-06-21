import os, sys, re

from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *

from pw_multiScriptEditor import scriptEditor
reload(scriptEditor)

q3dsmax = QApplication.instance()

class MaxDialogEvents(QObject):
    def eventFilter(self, obj, event):
        import MaxPlus
        if event.type() == QEvent.WindowActivate:
            MaxPlus.CUI.DisableAccelerators()
        elif event.type() == QEvent.WindowDeactivate:
            MaxPlus.CUI.EnableAccelerators()

        return False

def show():
    se = scriptEditor.scriptEditorClass(parent=None)
    se.installEventFilter(MaxDialogEvents())
    se.runCommand('import MaxPlus')
    se.MaxEventFilter = MaxDialogEvents()
    se.installEventFilter(se.MaxEventFilter)
    se.show()
