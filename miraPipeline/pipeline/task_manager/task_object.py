#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'

from miraLibs.dbLibs import db_api
from miraLibs.pipeLibs import pipeMira, get_current_project, pipeFile

import task_assets_object
reload(task_assets_object)

# sequences = st.get_sequence()
# shots = st.get_all_shots(sequence_name="s997")


class TaskObject(object):
    def __init__(self):
        super(TaskObject, self).__init__()
        '''init data'''
        self.__db = None
        self.asset_type = {}
        self.sequences = {}
        self.assets = {}
        self.asset_root = {}
        self.current_project = "SnowKidTest" # get_current_project.get_current_project()
        self.project = ''
        self.projects = pipeMira.get_projects()
        for per_project in self.projects:
            self.asset_root[per_project] = task_assets_object.AssetObject(per_project, '', '')
            self.set_project(per_project)

    def set_project(self, project):
        print 'set_project'
        self.project = project
        try:
            self.asset_type[project] = pipeMira.get_studio_value(self.project, "asset_type")
        except:
            self.assets[self.project] = {}
            raise Exception("Invalid Project!")
        else:
            try:
                self.__connect_db(project)
            except:
                pass
            else:
                # self.sequences[project] = self.__db.get_sequence()
                self.__get_all_assets()

    def __connect_db(self, project):
        print '__connect_db'
        try:
            self.__db = db_api.DbApi(project).db_obj
        except:
            self.assets[self.project] = {}
            raise Exception("Invalid Project Connect!")

    def __get_all_assets(self):
        print '__get_all_assets'
        # per_project_asset = []
        project_asset = {}
        for per_asset_type in self.asset_type[self.project]:
            asset_root = task_assets_object.AssetObject(per_asset_type, '', '', self.asset_root[self.project])
            per_asset_list = []
            asset_dict = {}
            for per_asset in self.__db.get_all_assets(asset_type=per_asset_type):
                asset_dict['name'] = per_asset['name']
                asset_dict['id'] = per_asset['id']
                workarea = pipeFile.get_entity_dir(self.project, "Asset", "workarea", per_asset_type, per_asset['name'])
                asset_dict['workarea'] = workarea
                publish = pipeFile.get_entity_dir(self.project, "Asset", "publish", per_asset_type, per_asset['name'])
                asset_dict['publish'] = publish

                task_assets_object.AssetObject(per_asset['name'], workarea, publish, asset_root)

                per_asset_list.append(asset_dict)
            project_asset[per_asset_type] = per_asset_list
        # per_project_asset.append(project_asset)
        self.assets[self.project] = project_asset

    def __get_all_shots(self):
        pass

    def get_assets(self, assets_type=''):
        return self.assets[assets_type]

    def assets_update(self):
        self.__get_all_assets()

if __name__ == "__main__":
    test = TaskObject()
    print test.assets
    print test.asset_type
    print test.asset_root




