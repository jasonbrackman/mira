#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_get_invalid_asset
# description : ''
# author      : Aaron Hui
# date        : 2015/12/31
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import re

# Third-party modules

# Studio modules

# Local modules
import add_environ
from sg_utils import get_sg

logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_get_invalid_asset_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def get_invalid_asset(project_id=68):
    invalid_asset = list()
    sg = get_sg.get_sg()
    all_assets = sg.find('Asset', [['project', 'is', {'type': 'Project', 'id': project_id}]], ['code'])
    pattern = re.compile(r'^[a-zA-Z0-9]+$')
    for asset in all_assets:
        asset_name = asset['code']
        if not re.match(pattern, asset_name):
            invalid_asset.append(asset_name)
    return invalid_asset


if __name__ == "__main__":
    pass
