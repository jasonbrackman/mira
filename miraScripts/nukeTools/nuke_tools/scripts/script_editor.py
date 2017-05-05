# -*- coding: utf-8 -*-
import sys
import getpass


def main():
    user = getpass.getuser()
    editor_path = "Z:/miraSG/miraTools"
    if user == "heshuai":
        editor_path = "E:/miraSG/miraTools"
    if editor_path not in sys.path:
        sys.path.append(editor_path)
    import pw_multiScriptEditor
    reload(pw_multiScriptEditor)
    pw_multiScriptEditor.showNuke()
