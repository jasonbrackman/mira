from miraLibs.stLibs import St
from miraLibs.mayaLibs import set_frame_range
from miraLibs.log import Log


def fix_frame_range(context):
    shot_name = "%s_%s" % (context.sequence, context.shot)
    st = St.St(context.project)
    frame_range = st.get_shot_task_frame_range(shot_name)
    if not frame_range:
        Log.warning("PA doesn't set the frame range")
        return
    start, end = frame_range.split("-")
    set_frame_range.set_frame_range(int(start), int(end))
