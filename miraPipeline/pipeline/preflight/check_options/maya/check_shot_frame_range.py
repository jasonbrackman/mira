# -*- coding: utf-8 -*-
from BaseCheck import BaseCheck
from miraLibs.mayaLibs import get_frame_range, set_frame_range
from miraLibs.pipeLibs import pipeFile
from miraLibs.stLibs import St


class check_shot_frame_range(BaseCheck):

    def run(self):
        self.db_frame_range = self.get_db_frame_range()
        current_frame_range = self.current_frame_range()
        if self.db_frame_range == current_frame_range:
            self.pass_check(u"帧范围正确。")
        else:
            self.fail_check(u"帧范围设置与strack设置不符")

    @staticmethod
    def current_frame_range():
        frame_range = get_frame_range.get_frame_range()
        start = int(frame_range[0])
        end = int(frame_range[1])
        return "%s-%s" % (start, end)

    @staticmethod
    def get_db_frame_range():
        context = pipeFile.PathDetails.parse_path()
        sequence = context.sequence
        shot = context.shot
        shot_name = "%s_%s" % (sequence, shot)
        st = St.St(context.project)
        frame_range = st.get_shot_task_frame_range(shot_name)
        return frame_range

    def auto_solve(self):
        start, end = self.db_frame_range.split("-")
        set_frame_range.set_frame_range(int(start), int(end))
        self.pass_check(u"已纠正帧范围。")
