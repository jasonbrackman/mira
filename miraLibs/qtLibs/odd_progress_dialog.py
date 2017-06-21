#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/21'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *

# Studio modules

# Local modules


QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


def odd_progress_dialog(num, info="处理中..."):
    """

    :param num: range max
    :param info: shown information
    :return: QProgressDialog
    """
    progress_dialog = QProgressDialog()
    progress_dialog.setWindowModality(Qt.WindowModal)
    progress_dialog.setMinimumDuration(5)
    progress_dialog.setWindowTitle(progress_dialog.tr("请等待"))
    progress_dialog.setLabelText(progress_dialog.tr(info))
    progress_dialog.setCancelButtonText(progress_dialog.tr("取消"))
    progress_dialog.setRange(0, num)
    return progress_dialog


if __name__ == "__main__":
    import sys
    import time
    app = QApplication(sys.argv)
    test_pd = odd_progress_dialog(100)
    for i in range(101):
        test_pd.setValue(i)
        time.sleep(0.05)
    app.exec_()
