# -*- coding: utf-8 -*-
import nuke


def quit_nuke(force=True):
    nuke.scriptExit(forceExit=force)
