# -*- coding: utf-8 -*-
from miraLibs.osLibs import get_parent_win
from miraFramework.PipelineBaseUI import PipelineBaseUI
from miraLibs.qtLibs.splash import splash


def normal_render(widget_class):
    parent_win = get_parent_win.get_parent_win()
    if parent_win:
        pb_ui = PipelineBaseUI(widget_class, parent_win)
        pb_ui.show()
    else:
        pb_ui = PipelineBaseUI(widget_class)
        pb_ui.show()
    return pb_ui


@splash
def render(widget_class):
    ui_object = normal_render(widget_class)
    return ui_object
