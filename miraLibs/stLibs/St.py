# -*- coding: utf-8 -*-
import getpass
from get_standalone_st import get_standalone_st


class St(object):
    def __init__(self, project_name=None):
        self.project_name = project_name
        self.st = get_standalone_st()
        self.user = getpass.getuser()
        self.typ = "strack"
        if self.project_name:
            self.project_id = self.get_project_by_name().get("id")

    @property
    def user_id(self):
        user_info = self.get_user_by_name(self.user)
        return user_info.get("id")

    def get_project_by_name(self):
        project_info = self.st.project.find(filters="name=%s" % self.project_name)
        return project_info

    def get_category_by_name(self, category_name):
        """
        get asset type information
        :param category_name: asset type
        :return:
        """
        category = self.st.category.find(filters="name=%s" % category_name)
        return category

    def get_step_by_id(self, step_id):
        step_info = self.st.step.find(filters="id=%s" % step_id, fields=["name"])
        return step_info

    def get_step_by_name(self, step_name):
        step_info = self.st.step.find(filters="name=%s" % step_name, fields=["id"])
        return step_info

    def get_status_by_name(self, status_name):
        status_info = self.st.status.find("name=%s" % status_name)
        return status_info

    def get_user_by_name(self, name):
        user = self.st.user.find(filters="name=%s" % name, fields=["email", "department.name"])
        return user

    def get_user_department(self, name):
        user_info = self.get_user_by_name(name)
        return user_info.get("department").get("name")

    def get_entity_info(self, entity_type, asset_type_or_sequence, asset_or_shot):
        if entity_type == "Asset":
            category_info = self.get_category_by_name(asset_type_or_sequence)
            category_id = category_info.get("id")
            asset_filters = "name=%s and category_id=%s and project_id=%s" % \
                            (asset_or_shot, category_id, self.project_id)
            entity_info = self.st.asset.find(filters=asset_filters)
        elif entity_type == "Shot":
            sequence_info = self.get_sequence_by_name(asset_type_or_sequence)
            sequence_id = sequence_info.get("id")
            shot_filters = "name=%s and sequence_id=%s and project_id=%s" % \
                           (asset_or_shot, sequence_id, self.project_id)
            entity_info = self.st.shot.find(filters=shot_filters)
        else:
            print "entity type is invalid."
            return
        return entity_info

    def get_sequence_by_name(self, sequence_name):
        sequence_filters = "project_id=%s and name=%s" % (self.project_id, sequence_name)
        sequence_info = self.st.sequence.find(filters=sequence_filters)
        return sequence_info

    def get_sequence(self):
        all_sequence = self.st.sequence.select(filters="project_id=%s" % self.project_id, fields=["name"])
        if not all_sequence:
            return
        all_sequence_name = [sequence['name'] for sequence in all_sequence]
        all_sequence_name.sort()
        return all_sequence_name

    def get_all_assets(self, asset_type=None):
        if asset_type is None:
            assets = self.st.asset.select(filters="project_id=%s" % self.project_id, fields=["name"])
        else:
            category = self.get_category_by_name(asset_type)
            filters = "project_id=%s and category_id=%s" % (self.project_id, category.get("id"))
            assets = self.st.asset.select(filters=filters, fields=["name"])
        return assets

    def get_all_shots(self, sequence_name=None):
        if not sequence_name:
            shots = self.st.shot.select(filters="project_id=%s" % self.project_id, fields=["name"])
        else:
            sequence_info = self.get_sequence_by_name(sequence_name)
            sequence_id = sequence_info.get("id")
            shots = self.st.shot.select(filters="sequence_id=%s" % sequence_id, fields=["name"])
            shots = [shot for shot in shots if '_000' not in shot['name']]
        return shots

    def get_task(self, entity_type, asset_type_or_sequence, asset_or_shot, step=None):
        entity_info = self.get_entity_info(entity_type, asset_type_or_sequence, asset_or_shot)
        if not entity_info:
            return
        if step:
            step_info = self.get_step_by_name(step)
            task_filters = "item_id=%s and step_id=%s" % (entity_info.get("id"), step_info.get("id"))
            tasks = self.st.task.select(filters=task_filters, fields=["name", "step.name"])
        else:
            task_filters = "item_id=%s" % entity_info.get("id")
            tasks = self.st.task.select(filters=task_filters, fields=["name", "step.name"])
        return tasks

    def get_step(self, entity_type, asset_type_or_sequence, asset_or_shot):
        tasks = self.get_task(entity_type, asset_type_or_sequence, asset_or_shot)
        if not tasks:
            return
        steps = [task.get("step").get("name") for task in tasks]
        return steps

    def get_users(self):
        users = self.st.user.select()
        return users

    def get_current_task(self, entity_type, asset_type_or_sequence, asset_or_shot, step, task_name):
        step_info = self.get_step_by_name(step)
        step_id = step_info.get("id")
        entity_info = self.get_entity_info(entity_type, asset_type_or_sequence, asset_or_shot)
        entity_id = entity_info.get("id")
        task_filters = "item_id=%s and step_id=%s and name=%s" % (entity_id, step_id, task_name)
        task_info = self.st.task.find(filters=task_filters, fields=["json", "status.color", "status.name"])
        return task_info

    def get_status_color(self, status_id):
        step_info = self.st.step.find("id=%s" % status_id, ["color"])
        return step_info.get("color")

    def get_current_user(self):
        import getpass
        user_name = getpass.getuser()
        return self.get_user_by_name(user_name)

    def get_my_tasks(self, user=None):
        if not user:
            user = self.user
        user_info = self.get_user_by_name(user)
        user_id = user_info.get("id")
        task_filters = "assignee=%s and project_id=%s" % (user_id, self.project_id)
        fields = ["item", "step.name", "status.name", "priority", "name", "due_date", "status.color"]
        my_tasks = self.st.task.select(filters=task_filters, fields=fields)
        return my_tasks

    def update_task_status(self, task, status):
        status_info = self.get_status_by_name(status)
        status_id = status_info.get("id")
        self.st.task.update(task.get("id"), {"status_id": status_id})

    def update_task(self, task, **kwargs):
        self.st.task.update(task.get("id"), kwargs)

    def upload_thumbnail(self, entity_info, image_path):
        self.upload(entity_info.get("type"), entity_info.get("id"), image_path)

    def create(self, entity_type, data):
        """
        :param entity_type: Asset Shot Sequence......
        :param data: is a dict of args
        :return:
        """
        if entity_type == "Asset":
            return self.st.asset.create(data=data)
        elif entity_type == "Shot":
            return self.st.shot.create(data=data)

    def upload(self, entity_type, entity_id, path):
        if entity_type == "task":
            self.st.task.upload(entity_id=entity_id, path=path)
        elif entity_type == "asset":
            self.st.asset.upload(entity_id=entity_id, path=path)
        elif entity_type == "shot":
            self.st.shot.upload(entity_id=entity_id, path=path)

    def get_asset_type_by_asset_id(self, asset_id):
        asset_info = self.st.asset.find("id=%s" % asset_id, ["category.name"])
        return asset_info.get("category").get("name")

    def get_sequence_by_shot_id(self, shot_id):
        shot_info = self.st.shot.find("id=%s" % shot_id, ["sequence.name"])
        return shot_info.get("sequence").get("name")

    @staticmethod
    def get_task_entity_type(task):
        if not task.__contains__("item"):
            return
        type_dict = {"shot": "Shot", "asset": "Asset"}
        task_entity_type = type_dict.get(task.get("item").get("type"))
        return task_entity_type

    def upload_version(self, task_info, media_path="", file_path=""):
        task_id = task_info.get("id")
        version = self.st.version.create(data={"task_id": task_id,
                                               "path": {"file": file_path, "media": media_path}})
        # update version user id
        # self.st.version.update(version.get("id"), {"user_id": self.user_id})
        if media_path:
            self.st.media.encoding(version.get("id"), media_path)

    def update_file_path(self, task_info, work_file_path="", publish_file_path=""):
        old_value = task_info.get("json")
        if not old_value:
            old_value = dict()
        if work_file_path:
            old_value["work_file_path"] = work_file_path
        if publish_file_path:
            old_value["publish_file_path"] = publish_file_path
        self.update_task(task_info, json=old_value)


if __name__ == "__main__":
    st = St("SnowKidTest")
    # for i in st.get_my_tasks():
    #     print i
    task = st.st.task.find("id=615", ["priority"])
    print task
    # st.update_task(task, current_version=10)
    # st.st.task.update(615, {"json": {"work_file_path": "W:/SnowKidTest/workarea/assets/Prop/TdTest/Hair/Hair/_workarea/maya/SnowKidTest_TdTest_Hair_Hair_v005.ma"}})
    # print st.get_current_task("Asset", "Prop", "TdTest", "MidMdl", "MidMdl")
    # print st.get_current_task("Shot", "s999", "s999_c001", "AnimLay", "AnimLay")
    # print st.st.task.relations

