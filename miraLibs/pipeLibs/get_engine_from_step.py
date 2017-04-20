# -*- coding: utf-8 -*-


def get_engine_from_step(step):
    engine = None
    if step in ["comp"]:
        engine = "nuke"
    elif step in ["lowMdl", "mdl", "lowRig", "rig", "shd", "hair",
                  "lay", "anim", "set", "cfx", "lgt", "sim"]:
        engine = "maya"
    return engine
