# -*- coding: utf-8 -*-
import getpass
from get_standalone_sg import get_standalone_sg


class Sg(object):
    def __init__(self, project=None):
        self.project_name = project
        self.sg = get_standalone_sg()
        self.user = getpass.getuser()
        self.typ = "shotgun"

    def get_project_by_name(self):
        project_info = self.sg.find_one('Project', [['name', 'is', self.project_name]], [])
        return project_info

    def get_sequence(self):
        sequence_filter = [['project', 'name_is', self.project_name]]
        all_sequence = self.sg.find('Sequence', sequence_filter, ['code'])
        if not all_sequence:
            return
        all_sequence_name = [sequence['code'] for sequence in all_sequence]
        all_sequence_name.sort()
        return all_sequence_name

    def get_all_assets(self, asset_type=None):
        if asset_type is None:
            assets = self.sg.find("Asset", [["project", "name_is", self.project_name]], ["code"])
        else:
            assets = self.sg.find("Asset",
                                  [["project", "name_is", self.project_name], ["sg_asset_type", "is", asset_type]],
                                  ["code"])
        return assets

    def get_all_shots(self, sequence_name=None):
        if not sequence_name:
            shots = self.sg.find("Shot", [['project', 'name_is', self.project_name]])
        else:
            sequence_info = self.sg.find_one('Sequence',
                                             [['project', 'name_is', self.project_name], ['code', 'is', sequence_name]],
                                             ['shots'])
            shots = [shot for shot in sequence_info['shots'] if '_000' not in shot['name']]
        return shots

    def get_task(self, entity_type, asset_type_or_sequence, asset_or_shot, step=None):
        if entity_type == "Asset":
            entity_info = self.sg.find_one("Asset",
                                           [["code", "is", asset_or_shot],
                                            ["sg_asset_type", "is", asset_type_or_sequence],
                                            ["project", "name_is", self.project_name]])
        elif entity_type == "Shot":
            entity_info = self.sg.find_one("Shot",
                                           [["code", "is", asset_or_shot],
                                            ["sg_sequence", "name_is", asset_type_or_sequence],
                                            ["project", "name_is", self.project_name]])
        if step:
            step_info = self.sg.find_one("Step", [["short_name", "is", step]])
            tasks = self.sg.find("Task", [["entity", "is", entity_info], ["step", "is", step_info]], ["content", "step"])
        else:
            tasks = self.sg.find("Task", [["entity", "is", entity_info]], ["content", "step.Step.short_name"])
        return tasks

    def get_step(self, entity_type, asset_type_or_sequence, asset_or_shot):
        tasks = self.get_task(entity_type, asset_type_or_sequence, asset_or_shot)
        if not tasks:
            return
        steps = [task["step.Step.short_name"] for task in tasks]
        return steps

    def get_users(self):
        users = self.sg.find("HumanUser", [["sg_status_list", "is", "act"], ["projects", "name_contains", self.project_name]], ["name"])
        return users

    def get_current_task(self, entity_type, asset_type_or_sequence, asset_or_shot, step, task_name):
        step_info = self.sg.find_one("Step", [["short_name", "is", step]])
        if entity_type == "Asset":
            entity_info = self.sg.find_one("Asset",
                                           [["code", "is", asset_or_shot],
                                            ["sg_asset_type", "is", asset_type_or_sequence],
                                            ["project", "name_is", self.project_name]])
        else:
            entity_info = self.sg.find_one("Shot",
                                           [["code", "is", asset_or_shot],
                                            ["sg_sequence", "name_is", asset_type_or_sequence],
                                            ["project", "name_is", self.project_name]])
        task_info = self.sg.find_one("Task",
                                     [["entity", "is", entity_info],
                                      ["step", "is", step_info],
                                      ["content", "is", task_name]],
                                     ["sg_workfile", "entity"])
        return task_info

    def get_user_by_name(self, name):
        user = self.sg.find_one("HumanUser", [["name", "is", name]], ["email"])
        return user

    def get_current_user(self):
        import getpass
        user_name = getpass.getuser()
        return self.get_user_by_name(user_name)

    def get_leader(self, user_info):
        user_filter = [["id", "is", user_info["id"]]]
        user = self.sg.find_one("HumanUser", user_filter, ["department"])
        if not user. has_key("department"):
            return
        user_dep_info = user["department"]
        user_dep_name = user_dep_info["name"]
        leader_dep_name = "%sLeader" % user_dep_name
        leaders = self.sg.find("HumanUser", [["department", "name_is", leader_dep_name]], ["email", "name"])
        return leaders

    def get_my_tasks(self, user=None):
        if not user:
            user = self.user
        task_filter = [["task_assignees", "name_contains", user], ["project", "name_is", self.project_name]]
        fields = ["content", "sg_status_list", "sg_priority_1", "step.Step.short_name", "entity.Asset.sg_asset_type",
                  "entity.Asset.code", "entity.Shot.sg_sequence", "entity.Shot.code", "entity"]
        my_tasks = self.sg.find("Task", task_filter, fields)
        return my_tasks

    def update_task_status(self, task, status):
        self.sg.update("Task", task["id"], {"sg_status_list": status})

    def update_task(self, task, **kwargs):
        self.sg.update("Task", task["id"], kwargs)

    def upload_thumbnail(self, task, image_path):
        self.sg.upload_thumbnail("Task", task["id"], image_path)

    def create(self, entity_type, data):
        return self.sg.create(entity_type, data)

    def upload(self, entity_type, entity_id, path, field=None):
        self.sg.upload(entity_type, entity_id, path, field)

    def get_department_of_user(self, user):
        user_info = self.get_user_by_name(user)
        return user_info.get("department").get("name")
