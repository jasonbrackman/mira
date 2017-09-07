# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import *
from miraLibs.pipeLibs import pipeFile, Step
from miraLibs.osLibs import FileOpener
from miraLibs.pyLibs import start_file


class Hook(object):
    def __init__(self, project, entity_type, asset_type_sequence, asset_shot_names, step, task, action_name):
        self.__project = project
        self.__entity_type = entity_type
        self.__asset_type_sequence = asset_type_sequence
        self.__asset_shot_names = asset_shot_names
        if isinstance(self.__asset_shot_names, basestring):
            self.__asset_shot_names = [self.__asset_shot_names]
        self.__step = step
        self.__task = task
        if self.__step:
            self.__engine = Step(self.__project, self.__step).engine
        self.__action_name = action_name

    def execute(self):
        if self.__action_name == "AR":
            self.ad_opt()
        elif self.__action_name == "Launch Folder":
            self.launch_folder()
        elif self.__action_name == "start":
            self.start()
        elif self.__action_name == "publish":
            self.publish()
        elif self.__action_name == "QA":
            self.quality_control()
        elif self.__action_name == "open":
            self.do_open()
        elif self.__action_name == "import":
            self.do_import()
        elif self.__action_name == "reference":
            self.do_reference()
        elif self.__action_name == "Launch Workarea":
            self.launch_workarea()
        elif self.__action_name == "Launch Publish":
            self.launch_publish()

    def ad_opt(self):
        from miraLibs.mayaLibs.Assembly import Assembly
        error_list = list()
        for name in self.__asset_shot_names:
            ad_file_path = pipeFile.get_asset_AD_file(self.__project, self.__asset_type_sequence, name)
            if not os.path.isfile(ad_file_path):
                error_list.append(ad_file_path)
                continue
            assemb = Assembly()
            assemb.reference_ad("%s_AR" % name, ad_file_path)
        if error_list:
            QMessageBox.warning(None, "Warming Tip", "%s \n\nis not an exist file." % "\n\n".join(error_list))

    def launch_folder(self):
        entity_dir = pipeFile.get_entity_dir(self.__project, self.__entity_type, "publish",
                                             self.__asset_type_sequence, self.__asset_shot_names[0])
        start_file.start_file(entity_dir)

    def start(self):
        pass

    def publish(self):
        pass

    def quality_control(self):
        work_file = pipeFile.get_task_work_file(self.__project, self.__entity_type, self.__asset_type_sequence,
                                                self.__asset_shot_names[0], self.__step, self.__task,
                                                engine=self.__engine)
        fo = FileOpener.FileOpener(work_file)
        fo.run()

    def maya_opt(self, opt):
        from miraLibs.mayaLibs import maya_import, create_reference, open_file
        error_list = list()
        for asset_shot_name in self.__asset_shot_names:
            publish_file = pipeFile.get_task_publish_file(self.__project, self.__entity_type,
                                                          self.__asset_type_sequence, asset_shot_name,
                                                          self.__step, self.__task, engine=self.__engine)
            if not publish_file or not os.path.isfile(publish_file):
                error_list.append(publish_file)
                continue
            if opt == "import":
                maya_import.maya_import(publish_file)
            elif opt == "reference":
                create_reference.create_reference(publish_file, asset_shot_name, True)
            elif opt == "open":
                open_file.open_file(publish_file)
        if error_list:
            QMessageBox.warning(None, "Warming Tip", "%s \n\nis not an exist file." % "\n\n".join(error_list))

    def do_open(self):
        self.maya_opt("open")

    def do_import(self):
        self.maya_opt("import")

    def do_reference(self):
        self.maya_opt("reference")

    def launch_workarea(self):
        work_file = pipeFile.get_task_work_file(self.__project, self.__entity_type, self.__asset_type_sequence,
                                                self.__asset_shot_names[0], self.__step, self.__task,
                                                version="000", engine=self.__engine)
        if not work_file:
            print "Maybe no format exist."
            return
        work_dir = os.path.dirname(work_file)
        if os.path.isdir(work_dir):
            start_file.start_file(work_dir)
        else:
            QMessageBox.warning(None, "Warming Tip", "%s \n\nis not an exist file." % work_dir)

    def launch_publish(self):
        publish_file = pipeFile.get_task_publish_file(self.__project, self.__entity_type, self.__asset_type_sequence,
                                                      self.__asset_shot_names[0], self.__step, self.__task,
                                                      engine=self.__engine)
        if not publish_file:
            print "Maybe no format exist."
            return
        publish_dir = os.path.dirname(publish_file)
        if os.path.isdir(publish_dir):
            start_file.start_file(publish_dir)
        else:
            QMessageBox.warning(None, "Warming Tip", "%s \n\nis not an exist file." % publish_dir)
