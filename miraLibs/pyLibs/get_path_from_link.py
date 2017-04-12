# -*- coding: utf-8 -*-
import win32com.client


def get_path_from_link(link_path):
    if link_path.endswith(".lnk"):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(link_path)
        path = shortcut.Targetpath
    else:
        path = link_path
    return path
