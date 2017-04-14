# -*- coding: utf-8 -*-
import getpass
from get_standalone_sg import get_standalone_sg


class Sg(object):
    def __init__(self, project=None):
        self.project_name = project
        self.sg = get_standalone_sg()
        self.user = getpass.getuser()

    def get_project_by_name(self):
        project_info = self.sg.find_one('Project', [['name', 'is', self.project_name]], [])
        return project_info

    def get_sequence(self):
        project_info = self.get_project_by_name()
        sequence_filter = [['project', 'is', project_info]]
        all_sequence = self.sg.find('Sequence', sequence_filter, ['code'])
        if not all_sequence:
            return
        all_sequence_name = [sequence['code'] for sequence in all_sequence]
        all_sequence_name.sort()
        return all_sequence_name

    def get_all_assets(self, asset_type=None):
        project_info = self.get_project_by_name()
        if asset_type is None:
            assets = self.sg.find("Asset", [["project", "is", project_info]], ["code"])
        else:
            assets = self.sg.find("Asset",
                                  [["project", "is", project_info], ["sg_asset_type", "is", asset_type]],
                                  ["code"])
        return assets

    def get_all_shots_by_sequence(self, sequence_name):
        project_info = self.get_project_by_name()
        sequence_info = self.sg.find_one('Sequence',
                                         [['project', 'is', project_info], ['code', 'is', sequence_name]],
                                         ['shots'])
        shots = [shot for shot in sequence_info['shots'] if '_000' not in shot['name']]
        return shots

    def get_task(self, entity_type, asset_type_or_sequence, asset_or_shot):
        project_info = self.get_project_by_name()
        if entity_type == "Asset":
            entity_info = self.sg.find_one("Asset",
                                           [["code", "is", asset_or_shot],
                                            ["sg_asset_type", "is", asset_type_or_sequence],
                                            ["project", "is", project_info]])
        elif entity_type == "Shot":
            sequence_info = self.sg.find_one("Sequence", [["project", "is", project_info],
                                                          ["code", "is", asset_type_or_sequence]])
            entity_info = self.sg.find_one("Shot",
                                           [["code", "is", asset_or_shot],
                                            ["sg_sequence", "is", sequence_info]])
        tasks = self.sg.find("Task", [["entity", "is", entity_info]], ["content"])
        return tasks

    def get_users(self):
        users = self.sg.find("HumanUser", [["sg_status_list", "is", "act"], ["projects", "name_contains", self.project_name]], ["name"])
        return users

    def get_current_task(self, entity_type, asset_type_or_sequence, asset_or_shot, step, task_name):
        project_info = self.get_project_by_name()
        step_info = self.sg.find_one("Step", [["short_name", "is", step]])
        if entity_type == "Asset":
            entity_info = self.sg.find_one("Asset",
                                           [["code", "is", asset_or_shot],
                                            ["sg_asset_type", "is", asset_type_or_sequence],
                                            ["project", "is", project_info]])
        else:
            sequence_info = self.sg.find_one("Sequence", [["project", "is", project_info],
                                                          ["code", "is", asset_type_or_sequence]])
            entity_info = self.sg.find_one("Shot",
                                           [["code", "is", asset_or_shot],
                                            ["sg_sequence", "is", sequence_info]])
        task_info = self.sg.find_one("Task",
                                     [["entity", "is", entity_info],
                                      ["step", "is", step_info],
                                      ["content", "is", task_name]])
        return task_info

    def get_user_by_name(self, name):
        user = self.sg.find_one("HumanUser", [["name", "is", name]], ["email"])
        return user

    def get_my_tasks(self, user=None):
        project_info = self.get_project_by_name()
        if not user:
            user = self.user
        task_filter = [["task_assignees", "name_contains", user], ["project", "is", project_info]]
        my_tasks = self.sg.find("Task", task_filter, ["content", "step", "sg_status_list", "entity", "sg_priority_1"])
        if my_tasks:
            for task in my_tasks:
                entity = task["entity"]
                entity_type = entity["type"]
                id_filter = [["id", "is", entity["id"]]]
                if entity_type == "Asset":
                    entity_info = self.sg.find_one(entity_type, id_filter, ["sg_asset_type", "code"])
                else:
                    entity_info = self.sg.find_one(entity_type, id_filter, ["sg_sequence", "code"])
                task["entity"] = entity_info
                step = task["step"]
                step_filter = [["id", "is", step["id"]]]
                step_info = self.sg.find_one("Step", step_filter, ["short_name"])
                task["step"] = step_info
        return my_tasks

    def update_task_status(self, task, status):
        self.sg.update("Task", task["id"], {"sg_status_list": status})
