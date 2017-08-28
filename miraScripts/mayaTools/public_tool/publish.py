import logging
import os
import imp
from Qt.QtWidgets import *
import miraCore
from miraLibs.pipeLibs import pipeFile


PASSWORD = "aierpingfang"


def main():
    # input dialog
    password, ok = QInputDialog.getText(None, "Enter a password", "Password", QLineEdit.Password)
    if not (password and ok):
        return
    if password != PASSWORD:
        logging.warning(u"Wrong Password")
        return
    context = pipeFile.PathDetails.parse_path()
    step = context.step
    pipeline_dir = miraCore.get_pipeline_dir()
    publish_dir = os.path.join(pipeline_dir, "maya", "publish").replace("\\", "/")
    fn_, path, desc = imp.find_module(step, [publish_dir])
    mod = imp.load_module(step, fn_, path, desc)
    mod.main(context.work_path, True)
