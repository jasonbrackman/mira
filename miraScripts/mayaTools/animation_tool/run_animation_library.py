# -*- coding: utf-8 -*-
import os, sys


def main():
    from miraScripts.mayaTools import animation_tool
    sys.path.insert(0, os.path.dirname(animation_tool.__file__))
    import studiolibrary
    studiolibrary.main()


if __name__ == "__main__":
    main()
