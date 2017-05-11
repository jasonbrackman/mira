#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_fix_rig
# description : ''
# author      : HeShuai
# date        : 2016/1/27
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import optparse
# Third-party modules

# Studio modules

# Local modules


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_fix_rig_log.txt'),
                    level=logging.WARN, filemode='w', format='%(asctime)s - %(levelname)s: %(message)s')


def fix_rig():
    import maya.cmds as mc
    # open file
    ext = os.path.splitext(options.file)[1]
    base_name = os.path.basename(options.file).split(".")[0]
    new_base_name = "%sbak%s" % (base_name, ext)
    new_os_name = os.path.abspath(os.path.join(os.path.dirname(options.file), new_base_name))
    if os.path.isfile(new_os_name):
        os.remove(new_os_name)
    mc.file(options.file, open=1, pmt=1)
    # bake file
    try:
        os.rename(options.file, new_os_name)
    except Exception as e:
        print "[AAS] error: %s" % (str(e))
    # fix rig
    try:
        mc.setAttr("R_Elbow_FK_Ctrl.rx", lock=1, keyable=0, channelBox=0)
    except:
        try:
            mc.setAttr("R_ElbowFK_Ctrl.rx", lock=1, keyable=0, channelBox=0)
        except Exception as e:
            print "[AAS] error: %s" % str(e)

    try:
        mc.setAttr("L_Elbow_FK_Ctrl.rx", lock=1, keyable=0, channelBox=0)
    except:
        try:
            mc.setAttr("L_ElbowFK_Ctrl.rx", lock=1, keyable=0, channelBox=0)
        except Exception as e:
            print "[AAS] error: %s" % str(e)

    try:
        mc.setAttr("R_Elbow_FK_Ctrl.rz", lock=1, keyable=0, channelBox=0)
    except:
        try:
            mc.setAttr("R_ElbowFK_Ctrl.rz", lock=1, keyable=0, channelBox=0)
        except Exception as e:
            print "[AAS] error: %s" % str(e)

    try:
        mc.setAttr("L_Elbow_FK_Ctrl.rz", lock=1, keyable=0, channelBox=0)
    except:
        try:
            mc.setAttr("L_Elbow_FKCtrl.rz", lock=1, keyable=0, channelBox=0)
        except Exception as e:
            print "[AAS] error: %s" % str(e)
    # save file
    mc.file(save=1)
    mc.quit(f=1)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="Maya file ma or mb", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    parser.add_option("-l", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -l\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["rig_file"] if i in dir()]) == 1:
        options.file = rig_file
        fix_rig()
