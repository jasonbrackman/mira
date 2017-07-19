# -*- coding: utf-8 -*-


def get_engine_from_step(step):
    engine = None
    if step in ["Art"]:
        return "photoshop"
    if step in ["Comp"]:
        engine = "nuke"
    elif step in ["LowMdl", "MidMdl", "HighMdl", "Shd", "MidRig", "Rig", "Hair", "Group", "HighRig"]:
        engine = "maya"
    return engine
