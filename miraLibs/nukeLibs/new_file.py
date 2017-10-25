# -*- coding: utf-8 -*-
import nuke


def new_file(force=True):
    nuke.scriptClose(ignoreUnsavedChanges=force)
