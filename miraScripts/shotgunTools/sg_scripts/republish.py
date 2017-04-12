#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/12/21
# version     :
# usage       :
# notes       :

# Built-in modules
import logging
import os
import re
import sys
# Third-party modules
core_path = os.path.abspath(r"Z:\Resource\Pipeline\app_config\sgtk\tank\install\core\python")
sys.path.append(core_path)

import sgtk
# Studio modules

# Local modules
import add_environ
from sg_utils import get_tk_object


asset_csv_path = 'D:/asset.csv'

logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'republish.txt'),
                    level=logging.DEBUG, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


class UsualUtility(object):

    @staticmethod
    def get_asset_names():
        with open(asset_csv_path) as f:
            asset_names = f.readlines()
        asset_names = [asset_name.strip('\r\n') for asset_name in asset_names]
        return asset_names

    @staticmethod
    def get_max_version_info(path):
        current_task_dir = os.path.dirname(path)
        if not os.path.isdir(current_task_dir):
            return
        if not os.listdir(current_task_dir):
            return
        padding_list = re.findall('_v(\d+)\.', path)
        if not padding_list:
            return
        padding = len(padding_list[0])
        path = path.replace('\\', '/')
        pattern = re.sub('_v\d{%s}\.' % padding, '_v(\d{%s})\.' % padding, path)
        # get all published versions
        versions = list()
        for published_file in os.listdir(current_task_dir):
            published_file_path = os.path.join(current_task_dir, published_file).replace('\\', '/')
            matched = re.match(pattern, published_file_path)
            if not matched:
                continue
            version_num = matched.group(1)
            versions.append(version_num)
        if versions:
            max_version = max([int(version) for version in versions])
            max_version_str = '_v'+str(max_version).zfill(padding)+'.'
            publish_file_name = re.sub('_v\d{%s}\.' % padding, max_version_str, path)
            publish_file_name = os.path.abspath(publish_file_name)
            return publish_file_name, max_version


class ShotgunUtility(object):
    def __init__(self):
        self.tk = get_tk_object.get_tk_object()
        self.sg = self.tk.shotgun

    def get_asset_by_name(self, asset_name):
        asset_info = self.sg.find_one('Asset', [['code', 'is', asset_name]], [])
        return asset_info

    def get_task(self, asset_info, task_type):
        task = self.sg.find_one('Task', [['entity', 'is', asset_info],
                                ['sg_task_type', 'name_contains', task_type]], ['content'])
        return task

    def get_mdl_task(self, asset_info):
        mdl_task = self.get_task(asset_info, 'mdl')
        return mdl_task

    def get_rig_task(self, asset_info):
        rig_task = self.get_task(asset_info, 'rig')
        return rig_task

    def get_task_path(self, task):
        template_name = 'maya_asset_publish'
        template = self.tk.templates[template_name]
        self.tk.create_filesystem_structure("Task", task['id'], engine="tk-maya")
        context = self.tk.context_from_entity('Task', task['id'])
        fields = context.as_template_fields(template)
        fields['version'] = 1
        task_path = template.apply_fields(fields)
        return task_path


def main():
    sg_utils = ShotgunUtility()
    asset_names = UsualUtility.get_asset_names()
    for asset_name in asset_names:
        asset_info = sg_utils.get_asset_by_name(asset_name)
        if not asset_info:
            logging.info('%s does not exist in shotgun' % asset_name)
            continue
        mdl_task = sg_utils.get_mdl_task(asset_info)
        if not mdl_task:
            logging.info('%s has no mdl task' % asset_name)
        rig_task = sg_utils.get_rig_task(asset_info)
        if not rig_task:
            logging.info('%s has no rig task' % asset_name)
        for task in [mdl_task, rig_task]:
            if not task:
                continue
            task_path = sg_utils.get_task_path(task)
            publish_file_info = UsualUtility.get_max_version_info(task_path)
            if publish_file_info:
                publish_file_name, version_number = publish_file_info
                args = {
                    "tk": sg_utils.tk,
                    "context": sg_utils.tk.context_from_path(publish_file_name),
                    "path": publish_file_name,
                    "name": os.path.basename(publish_file_name),
                    "version_number": version_number,
                    "created_by": {'type': 'HumanUser', 'id': 126},
                }
                try:
                    sgtk.util.register_publish(**args)
                    print "publish %s" % task['content']
                except Exception as e:
                    print "[AAS] error: %s" % str(e)
                    logging.error(str(e))


if __name__ == '__main__':
    main()
