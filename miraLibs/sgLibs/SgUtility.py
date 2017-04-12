# -*- coding: utf-8 -*-
from get_tk_object import get_tk_object


class SgUtility(object):
    def __init__(self, project_name):
        self.project_name = project_name
        self.tk = get_tk_object(project_name)
        self.sg = self.tk.shotgun

    def get_all_projects(self):
        projects = self.sg.find('Project', [], ['name'])
        projects = [project['name'] for project in projects]
        return projects

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

    def get_all_shots_by_sequence(self, sequence_name):
        project_info = self.get_project_by_name()
        sequence_info = self.sg.find_one('Sequence',
                                         [['project', 'is', project_info], ['code', 'is', sequence_name]],
                                         ['shots'])
        shots = [shot for shot in sequence_info['shots'] if '_000' not in shot['name']]
        return shots

    def get_task_info_by_task_name(self, task_name):
        project_info = self.get_project_by_name()
        task_info = self.sg.find_one("Task", [["project", "is", project_info], ["content", "is", task_name]], [])
        if task_info:
            try:
                self.tk.create_filesystem_structure("Task", task_info['id'], engine="tk-maya")
            except Exception as e:
                print "[AAS] error: %s" % str(e)
        return task_info

    def get_latest_published_of_task(self, task_name):
        task_info = self.get_task_info_by_task_name(task_name)
        latest_version_file, max_version_number = self.get_latest_published_of_task_info(task_info)
        return latest_version_file, max_version_number

    def get_latest_published_of_task_info(self, task_info):
        project_info = self.get_project_by_name()
        published_info_list = self.sg.find('PublishedFile',
                                           [['project', 'is', project_info], ['task', 'is', task_info]],
                                           ['path', 'version_number'])
        if not published_info_list:
            return
        max_version_number = None
        latest_version_file = None
        for published_info in published_info_list:
            if not max_version_number:
                max_version_number = published_info['version_number']
                latest_version_file = published_info['path']['local_path']
            if published_info['version_number'] > max_version_number:
                max_version_number = published_info['version_number']
                latest_version_file = published_info['path']['local_path']
        return latest_version_file, max_version_number

    def get_frame_range_by_shot(self, shot):
        shot_info = self.sg.find_one("Shot", [['id', 'is', shot['id']]], ['sg_cut_in', 'sg_cut_out'])
        first_frame, last_frame = (shot_info['sg_cut_in'], shot_info['sg_cut_out'])
        return first_frame, last_frame

    def get_shot_by_shot_name(self, shot_name):
        project_info = self.get_project_by_name()
        shot_info = self.sg.find_one("Shot", [["project", 'is', project_info], ["code", "is", shot_name]])
        return shot_info

    def get_frame_range_by_shot_name(self, shot_name):
        shot_info = self.get_shot_by_shot_name(shot_name)
        frame_range = self.get_frame_range_by_shot(shot_info)
        return frame_range

    def get_resolution(self):
        project = self.get_project_by_name()
        project_info = self.sg.find_one('Project', [['id', 'is', project['id']]], ['sg_resolutionrender'])
        resolution = project_info['sg_resolutionrender']
        width, height = resolution.split('x')
        return int(width), int(height)

    def get_shot_info_by_maya_file_path(self, path):
        context = self.tk.context_from_path(path)
        entity_info = context.entity
        return entity_info

    def get_fps(self):
        project = self.get_project_by_name()
        project_info = self.sg.find_one('Project', [['id', 'is', project['id']]], ['sg_fps'])
        fps = int(project_info['sg_fps'])
        return fps

    def get_current_category(self, file_name):
        context = self.tk.context_from_path(file_name)
        current_task = context.task
        task_info = self.sg.find_one('Task', [['id', 'is', current_task['id']]], ['sg_task_type'])
        category = task_info['sg_task_type']['name']
        return category

    def get_current_step(self, file_name):
        context = self.tk.context_from_path(file_name)
        step = context.step
        step_info = self.sg.find_one("Step", [["id", "is", step["id"]]], ["short_name"])
        return step_info.get("short_name")

    # for fix rig work and publish file
    def get_all_assets(self, asset_type=None):
        project_info = self.get_project_by_name()
        if asset_type is None:
            assets = self.sg.find("Asset", [["project", "is", project_info]], ["code"])
        else:
            assets = self.sg.find("Asset",
                                  [["project", "is", project_info], ["sg_asset_type", "is", asset_type]],
                                  ["code"])
        return assets

    def get_all_asset_rig_tasks(self, asset_type=None):
        assets = self.get_all_assets(asset_type)
        rig_tasks = list()
        for asset in assets:
            rig_task = self.sg.find_one("Task",
                                        [["entity", "is", asset], ["sg_task_type", "name_is", "rig"]],
                                        ["content"])
            if not rig_task:
                print "%s has no rig task" % asset["code"]
                continue
            rig_tasks.append(rig_task)
        return rig_tasks


