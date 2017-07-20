#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'

import subprocess
import os
import yaml


def build_command_as_list(*args):
    return list(args)


def send_command(commands):
    #     commands = command(command_tool_path)
    #     print commands
    #     receiver = 'zhaopeng heshuai'
    #     message = 'dsdsdsdsdsd'
    #     add = '{command_tool_path} sendpopupmessage'.format(**vars())
    #     print add

    process = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    a = process.communicate()[0]
    print a


def send_message(receiver=[], message=''):
    command_tool_path = os.path.abspath(os.path.join(load_yaml(), 'deadlinecommand.exe'))
    if os.path.isfile(command_tool_path):
        send_command(build_command_as_list(command_tool_path, 'SendPopUpMessage', ','.join(receiver), message))


def create_job(**kwargs):
    info = []
    for key, value in kwargs.iteritems():
        info.append("%s=%s" % (key, value))

    info = ["%s\n" % k for k in info]
    with open('%s/job_info.job' % os.getenv('TEMP'), 'w') as f:
        f.writelines(info)

    return os.path.abspath('%s/job_info.job' % os.getenv('TEMP'))


def create_plugin(**kwargs):
    info = []
    for key, value in kwargs.iteritems():
        info.append("%s=%s" % (key, value))

    info = ["%s\n" % k for k in info]

    with open('%s/plugin_info.job' % os.getenv('TEMP'), 'w') as f:
        f.writelines(info)
    return os.path.abspath('%s/plugin_info.job' % os.getenv('TEMP'))


def submit_python_job(deadline_name,
                      script_file,
                      arguments,
                      machine_name,
                      user_name,
                      group='none',
                      pool='none',
                      priority=100,
                      version='2.7',
                      ):

    command_tool_path = os.path.abspath(os.path.join(load_yaml(), 'deadlinecommand.exe'))
    if os.path.isfile(command_tool_path):
        send_command(build_command_as_list(command_tool_path, create_job(Plugin='Python',
                                                                         Name=deadline_name,
                                                                         SynchronizeAllAuxiliaryFiles=True,
                                                                         Frames=1,
                                                                         Group=group,
                                                                         Pool=pool,
                                                                         Priority=priority,
                                                                         MachineName=machine_name,
                                                                         Whitelist=machine_name,
                                                                         UserName=user_name,
                                                                         ),
                                           create_plugin(ScriptFile=script_file,
                                                         Arguments=arguments,
                                                         Version=version,
                                                         )
                                           )
                     )


def submit_maya_script_job(deadline_name,
                           file_name,
                           machine_name,
                           user_name,
                           script_file,
                           group='none',
                           pool='none',
                           priority=100,
                           version='2016',
                           build='64bit',
                           project_path='W:/',
                           ):
    command_tool_path = os.path.abspath(os.path.join(load_yaml(), 'deadlinecommand.exe'))
    if os.path.isfile(command_tool_path):
        send_command(build_command_as_list(command_tool_path, create_job(Plugin='MayaBatch',
                                                                         Name=deadline_name,
                                                                         SynchronizeAllAuxiliaryFiles=True,
                                                                         Frames=1,
                                                                         Group=group,
                                                                         Pool=pool,
                                                                         Priority=priority,
                                                                         MachineName=machine_name,
                                                                         UserName=user_name,
                                                                         ),
                                           create_plugin(SceneFile=file_name,
                                                         Version=version,
                                                         Build=build,
                                                         ProjectPath=project_path,
                                                         StrictErrorChecking=True,
                                                         ScriptJob=True,
                                                         ScriptFilename=script_file,
                                                         )
                                           )
                     )


def load_yaml():
    yml_path = os.path.abspath(os.path.join(__file__, '..\deadline.yml'))
    if os.path.isfile(yml_path):
        with open(yml_path) as f:
            return yaml.load(f)['Command']


def main():
    # send_message(['zhaopeng', 'xiedonghang', 'heshuai'], 'nihao aaa')
    # submit_maya_script_job('deadline_test','W:/sct/assets/character/xiaotuotuo/shd/default/_workarea/sct_xiaotuotuo_shd_v013.mb','pipemanager','pipemanager','Z:/mira/miraScripts/pipeTools/publish/shd_publish.py')
    submit_python_job(u'deadline_python_test', r'Z:\mira\miraScripts\pipeTools\background_operate\deadtest.py',
                      u'sdsd 45',u'xiedonghang', u'pipemanager')

if __name__ == '__main__':
    main()
