#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_aas
# description : ''
# author      : HeShuai
# date        : 2016/1/12
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import sys
import subprocess
import optparse
import re
import tempfile

# Third-party modules

# Studio modules

# Local modules
import utility


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_aas_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def get_os_type():
    if 'win' in sys.platform:
        os_type = 'windows'
    elif 'linux' in sys.platform:
        os_type = 'linux'
    else:
        os_type = 'mac'
    return os_type


def kill_all():
    os.system("tskill maya")
    os.system("tskill mayabatch")
    os.system("tskill mayapy")
    os.system("tskill render")
    os.system("tskill python")
    os.system("tskill kick")


def run_command(cmd):
    print '[AAS] info: Running command: %s' % cmd
    os_type = get_os_type()
    if os_type == 'windows':
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    elif os_type == 'linux':
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    while True:
        return_code = p.poll()
        if return_code == 0:
            break
        elif return_code == 1:
            raise Exception('%s was crashed for some reason' % cmd)
        elif return_code is not None:
            raise Exception('%s was crashed for some reason' % cmd)
        line = p.stdout.readline()
        yield line


def export_frames(layer=None):
    """
    export all the frames in renderable layers
    Returns:
    """
    import maya.cmds as mc
    import pymel.core as pm
    pm.openfile(options.file, f=1, pmt=1)
    os_type = get_os_type()
    if os_type == "windows":
        project_path = os.path.join(tempfile.gettempdir(), 'projects')
    else:
        project_path = os.path.join('/tmp', "projects")
    if not os.path.isdir(project_path):
        os.makedirs(project_path)
    project = pm.workspace
    project.open(project_path)
    # get the renderable layers
    if layer is None:
        layers = [layer for layer in pm.ls(type='renderLayer')
                  if layer.renderable.get() and "defaultRenderLayer" not in layer.name()]
    else:
        layers = [pm.PyNode(layer)]
    #   some maya file missing beauty aov when export ass.
    try:
        import mtoa.aovs as aovs
        aovs.AOVInterface().addAOV('beauty')
    except:pass

    for layer in layers:
        print "[EXPORT] info:  export render layer %s " % layer
        pm.editRenderLayerGlobals(crl=layer)
        render_settings = pm.PyNode("defaultRenderGlobals")
        render_settings.animation.set(1)
        render_settings.extensionPadding.set(4)
        render_settings.outFormatControl.set(0)
        render_settings.putFrameBeforeExt.set(1)
        render_settings.periodInExt.set(1)

        driver = pm.PyNode("defaultArnoldDriver")
        driver.aiTranslator.set("exr")
        driver.tiled.set(0)
        driver.exrCompression.set(2)
        driver.mergeAOVs.set(1)

        for frame in range(int(options.start), int(options.end)+1):
            pm.currentTime(frame)
            pm.exportAll(os.path.join(project_path, "data", layer, str(frame).zfill(4)+'.ass'), type='AAS', f=1)
    print '[EXPORT] info: export ass files completed'
    mc.quit(f=1)


def export_start(use_mayapy=0):
    os_type = get_os_type()
    this = __file__.replace('\\', '/')
    options.file = options.file.replace('\\', '/')
    if use_mayapy:
        mayapy = utility.get_maya_py(options.file)
        cmd = "\"%s\" %s -f %s -s %s -e %s " % (mayapy, this, options.file, options.start, options.end)
    else:
        if options.use_version:
            mayabatch = "C:/tools/Autodesk/Maya%s/bin/mayabatch.exe" % options.use_version
        else:
            mayabatch = utility.get_maya_batch(options.file)
        if options.fix_nhair:
            if os_type == "win":
                cmd = "\"%s\" -command \"python \\\"ass_file='%s';" \
                      "ass_start=%s;ass_end=%s;render_layer='%s';" \
                      "fix_nhair='%s';execfile('%s')\\\"\"" % \
                      (mayabatch, options.file, options.start, options.end,
                       options.render_layer, options.fix_nhair, this)
            else:
                cmd = "%s -command \"python \\\"ass_file=\\\\\\\"%s\\\\\\\";" \
                      "ass_start=%s;ass_end=%s;render_layer=\\\\\\\"%s\\\\\\\";" \
                      "fix_nhair=\\\\\\\"%s\\\\\\\";" \
                      "execfile(\\\\\\\"%s\\\\\\\")\\\"\"" % \
                      (mayabatch, options.file, options.start, options.end,
                       options.render_layer, options.fix_nhair, this)
        else:
            if os_type == "win":
                cmd = "\"%s\" -command \"python \\\"ass_file='%s';" \
                      "ass_start=%s;ass_end=%s;render_layer='%s';execfile('%s')\\\"\"" % \
                      (mayabatch, options.file, options.start, options.end,
                       options.render_layer, this)
            else:
                cmd = "%s -command \"python \\\"ass_file=\\\\\\\"%s\\\\\\\";" \
                      "ass_start=%s;ass_end=%s;render_layer=\\\\\\\"%s\\\\\\\";" \
                      "execfile(\\\\\\\"%s\\\\\\\")\\\"\"" % \
                      (mayabatch, options.file, options.start, options.end,
                       options.render_layer, this)
    print "[AAS] info: Run export ass file command:"
    print cmd
    out_ass = []
    RE_ASS = re.compile(r'.+\[ass\] writing (scene to )?(.+.ass).+')
    RE_ASS2 = re.compile(r'^Result: \'?(.+\.ass)\'?')
    for line in run_command():
        if options.is_verbose():
            if line.strip():
                print line.strip()
            r = RE_ASS.findall(line)
            if r:
                out_ass.append(r[0][1])
            else:
                r = RE_ASS2.findall(line)
                if r:
                    out_ass.append(r[0])
        else:
            if line.startswith("RuntimeError:"):
                print line.strip()
                raise Exception("Error found")
            elif line.startswith("Warning: Did not find a renderable camera"):
                print line.strip()
                raise Exception("Camera not found")
            elif RE_ASS.findall(line):
                print line.strip()
                out_ass.append(RE_ASS.findall(line)[0][1])
            elif RE_ASS2.findall(line):
                print line.strip()
                out_ass.append(RE_ASS2.findall(line)[0])
            elif "backtrace" in line:
                kill_all()
                raise Exception("Arnold crashed")
            elif "access violation" in line:
                kill_all()
                raise Exception("Arnold crashed")

    out_ass = [j for i in out_ass for j in i.split()]
    return set(out_ass)


def render_frame(frame):
    frame = str(frame)
    if options.use_version:
        options.version = int(options.use_version)
    kick = utility.get_arnold_kick(options.version)
    shader = utility.get_arnold_shader(options.version)
    mtoa_shader = utility.get_arnold_default_shader(options.version)
    inputs = {}
    for i in options.input.split(','):
        inputs[i] = frame.zfill(i.count('#'))
    input = " ".join([re.sub(r'#+', inputs[i], i) for i in inputs])
    #argument nocrashpopup is only availble on windows.



def start():
    print "start"


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.set_usage("\n" \
                     "normal \"python scriptname -f file -r renderpath -s start -e end\"\n" \
                     "normal \"python scriptname -f file -r renderpath -l renderlayer -s start -e end\"\n" \
                     "poster \"python scriptname -f file -r renderpath -s start -e end -t tiles -I index\"\n" \
                     "test   \"python scriptname --test\"")
    parser.add_option("-i", dest="input",
                      help="input ass file path use '.' to separate" \
                      "such as: -i char.####.ass.gz, env.####.ass",
                      metavar="string")
    parser.add_option("-s", dest="start",
                      help="start frame",
                      metavar="int")
    parser.add_option("-e", dest="end",
                      help="end_frame",
                      metavar="int")
    parser.add_option("-v", dest="version",
                      help="Maya Version",
                      metavar="int")
    parser.add_option("--use_version", dest="use_version",
                      help="use specific maya version",
                      metavar="int")
    parser.add_option("--fix_nhair", dest="fix_nhair",
                      help="fix nhair cache location error",
                      metavar="int")
    parser.add_option("-o", dest="ouput",
                      help="output image path such as: -o shot.####.exr",
                      metavar="string")
    parser.add_option("-p", dest="parameters",
                      help="override some ass parameters, use ',' " \
                           "to seperate, such as : -p " \
                           "options.camera=WG_CG2_S07f0Shape1," \
                           "defaultArnoldDriver@driver_exr.N.filename=" \
                           "V:/dragon/scripts/temp/images/n/####.exr",
                      metavar="string")
    parser.add_option("-d",
                      action="store_true", dest="is_delete_ass", default=0,
                      help="If set this args, " \
                           "script would be delete the ass files after " \
                           "render completed")
    parser.add_option("-f", dest="file",
                      help="Maya file ma or mb",
                      metavar="string")
    parser.add_option("-r", dest="render_path",
                      help="render image path",
                      metavar="string")
    parser.add_option("-l", dest="render_layer",
                      help="render layer name",
                      metavar="string")
    parser.add_option("-t", dest="tiles",
                      help="poster tiles",
                      metavar="int")
    parser.add_option("-I", dest="index",
                      help="poster tile index",
                      metavar="int")
    parser.add_option("-V", action="store_true", dest="is_verbose", default=0,
                      help="show verbose export ass files log messages")
    parser.add_option("--rv", dest="render_verbose", default=4,
                      help="kick render verbose", metavar="int")
    parser.add_option("--test", action="store_true", dest="is_test", default=0,
                      help="mayapy.exe of maya2012 would be crashed in some " \
                           "machine, with unknown reason. we need find " \
                           "out these machine")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    parser.add_option("-b", dest="command2",
                      help="Not a needed argument, just for maya.bin, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -b\"",
                      metavar="string")
    options, args = parser.parse_args()

    if all((options.file, options.render_path, options.start, options.end)):
        start()
    elif all((options.file, options.start, options.end)):
        export_frames()
    elif all((options.input, options.version, options.start, options.end)):
        render_start()
    elif len([i for i in ["ass_file", "ass_start", "ass_end"]
              if i in dir()]) == 3:
        if "fix_nhair" in dir():
            options.fix_nhair = fix_nhair
        options.file = ass_file
        options.start = ass_start
        options.end = ass_end
        export_frames(layer=render_layer)
    else:
        parser.print_help()

