# -*- coding: utf-8 -*-
import nuke


def open_file(file_name):
    nuke.scriptClose(ignoreUnsavedChanges=True)
    nuke.scriptOpen(file_name)
