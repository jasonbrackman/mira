# -*- coding: utf-8 -*-
import sys
import os


def main():
    mira_dir = os.path.abspath(os.path.join(__file__, "..", "..", "..", ".."))
    sys.path.append(mira_dir)
    import send_command_ui
    reload(send_command_ui)
    send_command_ui.main()


if __name__ == "__main__":
    main()



