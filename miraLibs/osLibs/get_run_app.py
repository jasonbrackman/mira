# -*- coding: utf-8 -*-
import os
import sys


def get_run_app():
    app = sys.executable
    app_basename = os.path.basename(app)
    app_name = os.path.splitext(app_basename)[0]
    return app_name
