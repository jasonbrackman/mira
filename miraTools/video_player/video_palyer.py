# -*- coding: utf-8 -*-
import re
import os
import sys
import tempfile
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import VideoPlayerUI
from utility.get_children_files import get_children_files
from utility.get_conf_data import get_valid_ext


class VideoPlayer(VideoPlayerUI.VideoPlayerUI):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.frame_ratio = 24
        self.__run_mode = " normal"
        self.set_style_sheet()
        self.set_signals()

    def set_style_sheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
        self.setStyle(QStyleFactory.create('plastique'))
        with open(qss_path, "r") as f:
            self.setStyleSheet(f.read())

    def set_signals(self):
        self.set_frame_ratio_action.triggered.connect(self.set_frame_ratio)
        self.switch_to_normal_action.triggered.connect(self.switch_to_normal)
        self.exit_action.triggered.connect(self.do_close)
        self.collapse_btn.clicked.connect(self.do_collapse)
        self.expand_btn.clicked.connect(self.do_expand)
        self.file_list.list_view.clicked.connect(self.show_in_table)
        self.file_table.table_view.doubleClicked.connect(self.play_in_video)
        self.file_table.data_changed.connect(self.play_queue)
        self.pipeline_action.triggered.connect(self.work_for_pipeline)
        self.video.video_widget.drop.connect(self.on_video_widget_drop)

    def do_close(self):
        self.close()
        sys.exit(0)

    def set_frame_ratio(self):
        value, ok = QInputDialog.getInteger(self, "Set Frame Ratio", "Frame Ratio:", self.frame_ratio)
        if ok:
            self.frame_ratio = value
            self.video.set_frame_ratio(value)
            self.status_bar.showMessage("Current frame ratio: %s" % self.frame_ratio)

    def switch_to_normal(self):
        self.__run_mode = "normal"

    def do_collapse(self):
        self.collapse_widget.hide()
        self.file_widget.hide()
        self.expand_widget.show()
        self.main_splitter.setSizes([self.height(), 0])

    def do_expand(self):
        self.collapse_widget.show()
        self.file_widget.show()
        self.expand_widget.hide()
        self.main_splitter.setSizes([self.height()*0.75, self.height()*0.25])

    def on_video_widget_drop(self, data):
        self.file_table.add_column(data)

    def show_in_table(self, index):
        data = index.model().data(index)
        if self.__run_mode == "pipeline":
            self.show_in_table_pipeline(data)
        else:
            valid_ext = get_valid_ext()
            children_files = get_children_files(data, valid_ext)
            self.file_table.set_table_view(children_files)

    def work_for_pipeline(self):
        import PipelineWidget
        self.status_bar.showMessage("Current mode: pipeline.")
        self.__run_mode = "pipeline"
        pipeline_widget = PipelineWidget.PipelineWidget(self)
        pipeline_widget.show()
        pipeline_widget.play_clicked.connect(self.show_in_file_list)

    def show_in_file_list(self, data):
        self.do_expand()
        project = data["project"]
        sequence = data["sequence"]
        shots = data["shots"]
        context = data["context"]
        text_string = 'project: %s\n' \
                      'sequence: %s\n' \
                      'shots: %s\n' \
                      'context: %s' % (project, sequence, shots, context)
        self.file_list.set_list_view([text_string])

    def show_in_table_pipeline(self, data):
        from miraLibs.pipeLibs import pipeFile
        pattern = "^project: (.*)\nsequence: (.*)\nshots: (.*)\ncontext: (.*)"
        matched = re.match(pattern, data)
        project = matched.group(1)
        sequence = matched.group(2)
        shots = matched.group(3)
        context = matched.group(4)
        if context != "newest":
            video_paths = list()
            invalid_paths = list()
            for shot in shots.split(","):
                video_path = pipeFile.get_shot_step_video_file(sequence, shot, context, project)
                if os.path.isfile(video_path):
                    video_paths.append(video_path)
                else:
                    invalid_paths.append(video_path)
            if not video_paths:
                self.status_bar.showMessage("Warning: No files found.")
                return
            if invalid_paths:
                self.status_bar.showMessage("Invalid Paths:%s" % ",".join(invalid_paths))
        else:
            shot_contexts = ["comp", "lgt", "sim", "anim"]
            video_paths = list()
            for shot in shots.split(","):
                for each_context in shot_contexts:
                    newest_file = pipeFile.get_shot_step_video_file(sequence, shot, each_context, project)
                    if os.path.isfile(newest_file):
                        video_paths.append(newest_file)
                        break
            if not video_paths:
                self.status_bar.showMessage("Warning: No files found.")
                return
        video_paths.sort()
        self.status_bar.showMessage("Playing")
        self.file_table.set_table_view(video_paths)

    def play_in_video(self, index):
        column = index.column()
        self.video.player.clear()
        self.video.player.enqueue(self.video.queue)
        self.video.player.setCurrentSource(self.video.queue[column])
        self.video.play_when_loop()

    def play_queue(self):
        all_files = self.file_table.model_data
        if not all_files[0]:
            self.video.player.stop()
        else:
            self.video.set_source(all_files[0])

    def closeEvent(self, event):
        temp_dir = tempfile.gettempdir()
        for f in os.listdir(temp_dir):
            if f.startswith("video_") and f.endswith(".png"):
                try:
                    os.remove(os.path.join(temp_dir, f))
                except:pass

    def moveEvent(self, event):
        self.video.volume_widget_move()
        event.accept()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.video.set_full_screen(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    vp = VideoPlayer()
    vp.show()
    app.exec_()
