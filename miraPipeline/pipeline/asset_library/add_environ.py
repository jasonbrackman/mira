# -*- coding: utf-8 -*-
import os
import sys


package_dir = os.path.abspath(os.path.join(__file__, "..")).replace("\\", "/")
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)
