# -*- coding: utf-8 -*-
import sys
import os
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


def splash(func):
    def _wrapper(*args, **kwargs):
        # display exit splash screen
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        pixmap_path = os.path.join(__file__, "..", "splash.png")
        splash_pix = QPixmap(pixmap_path)
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        QCoreApplication.processEvents()
        result = func(*args, **kwargs)
        splash.close()
        try:
            sys.exit(app.exec_())
        except:pass
        return result
    return _wrapper


@splash
def tka():
    import time
    time.sleep(1)
    return 1


if __name__ == "__main__":
    print tka()