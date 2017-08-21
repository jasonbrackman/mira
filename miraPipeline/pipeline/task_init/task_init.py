import os
import imp
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
import miraCore
from ui import TaskUI
from miraLibs.pipeLibs import pipeFile
from miraLibs.osLibs import get_engine
from miraLibs.pipeLibs.pipeDb import task_from_db_path
from miraLibs.pyLibs import join_path


class TaskInit(TaskUI):
    def __init__(self, parent=None):
        super(TaskInit, self).__init__(parent)
        self.set_signals()
        self.selected = None
        self.__engine = get_engine.get_engine()
        self.__db = self.my_task_widget.db

    def show_task(self, item):
        self.info_label.setText("<font face=Courier New size=4><b>%s - %s - %s - %s - %s</b></font>"
                                % (item.entity_type, item.asset_type_sequence,
                                   item.asset_name_shot, item.step, item.task))

    def set_signals(self):
        self.my_task_widget.task_view.pressed.connect(self.on_task_pressed)
        
    def on_task_pressed(self, index):
        self.selected = index.data()
        self.show_task_info()
        self.set_dir()

    def show_task_info(self):
        self.show_task(self.selected)
    
    def init_task(self):
        work_file = pipeFile.get_task_work_file(self.selected.project, self.selected.entity_type,
                                                self.selected.asset_type_sequence, self.selected.asset_name_shot,
                                                self.selected.step, self.selected.task, version="001",
                                                engine=self.__engine)
        context = pipeFile.PathDetails.parse_path(work_file)
        local_file = context.local_work_path
        if os.path.isfile(local_file):
            msg = QMessageBox.information(self, "Warming Tip", "%s already exist\nDo you want to replace it?" % local_file,
                                          QMessageBox.Yes | QMessageBox.No)
            if msg.name == "No":
                return
            else:
                self.do_init_task(self.selected, local_file)
        else:
            self.do_init_task(self.selected, local_file)

    def do_init_task(self, step, local_file):
        pipeline_dir = miraCore.get_pipeline_dir()
        start_dir = os.path.join(pipeline_dir, self.__engine, "start").replace("\\", "/")
        fn_, path, desc = imp.find_module(step, [start_dir])
        mod = imp.load_module(step, fn_, path, desc)
        mod.main(local_file, True)
        self.update_task_status(local_file)

    def update_task_status(self, file_path):
        task = task_from_db_path.task_from_db_path(self.__db, file_path)
        self.__db.update_task_status(task, "In progress")
        self.__logger.info("Change task status to In progress.")
        from datetime import datetime
        now_time = datetime.now().strftime('%Y-%m-%d')
        self.__db.update_task(task, sub_date=now_time)
        self.__logger.info("Change task sub date: %s" % now_time)
    
    def set_dir(self):
        print self.selected.project, self.selected.entity_type,self.selected.asset_type_sequence, self.selected.asset_name_shot,self.selected.step, self.selected.task,
        local_file = pipeFile.get_task_work_file(self.selected.project, self.selected.entity_type,
                                                 self.selected.asset_type_sequence, self.selected.asset_name_shot,
                                                 self.selected.step, self.selected.task, "000",
                                                 engine=self.__engine, local=True)
        print local_file
        work_file = pipeFile.get_task_work_file(self.selected.project, self.selected.entity_type,
                                                self.selected.asset_type_sequence, self.selected.asset_name_shot,
                                                self.selected.step, self.selected.task, "000", engine=self.__engine)
        publish_file = pipeFile.get_task_publish_file(self.selected.project, self.selected.entity_type,
                                                      self.selected.asset_type_sequence, self.selected.asset_name_shot,
                                                      self.selected.step, self.selected.task, "000",
                                                      engine=self.__engine)
        local_dir = os.path.dirname(os.path.dirname(local_file))
        work_dir = os.path.dirname(os.path.dirname(work_file))
        publish_dir = os.path.dirname(os.path.dirname(publish_file))
        if self.__engine != "python":
            local_dir = join_path.join_path2(local_dir, self.__engine)
            work_dir = join_path.join_path2(work_dir, self.__engine)
            publish_dir = join_path.join_path2(publish_dir, self.__engine)
        self.local_list.set_dir(local_dir)
        self.work_list.set_dir(work_dir)
        self.publish_list.set_dir(publish_dir)
        

if __name__ == "__main__":
    from miraLibs.qtLibs import render_ui
    render_ui.render(TaskInit)
    # local_file = pipeFile.get_task_work_file("SnowKidTest", "Asset", "Prop", "TdTest", "MidMdl", "MidMdl", "000", "maya", True)
    # print local_file