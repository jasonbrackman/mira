#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       : aas_repos_parser
# description : ''
# author      : HeShuai
# date        : 2016/1/13
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import logging
import re
# Third-party modules

# Studio modules

# Local modules
import add_environ
import aas_libs.aas_sg as aas_sg
reload(aas_sg)

logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'aas_repos_parser_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


def parse_shot(text, project_name):
    sg_utils = aas_sg.SgUtility()
    all_sequence = sg_utils.get_sequence(project_name)
    all_shots = list()
    invalid_input = list()
    tongpei_pattern = r"^\d+[a-z]?_\*$"
    range_pattern = r"^\d+[a-z]?_\d+-\d+[a-z]?_\d+"
    single_pattern = r"^\d+[a-z]?_\d+"
    shot_string_list = text.split(',')
    for shot_string in shot_string_list:
        if not shot_string:
            continue
        # tong pei fu shots
        if re.match(tongpei_pattern, shot_string):
            sequence_name = shot_string.split('_')[0]
            if sequence_name not in all_sequence:
                invalid_input.append(shot_string)
            else:
                shots = sg_utils.get_all_shots_by_sequence(project_name, sequence_name)
                shot_names = [shot['name'] for shot in shots]
                all_shots.extend(shot_names)
        # range shots
        elif re.match(range_pattern, shot_string):
            shot_range = shot_string.split('-')
            if shot_range[0].split('_')[0] != shot_range[1].split('_')[0]:
                invalid_input.append(shot_string)
                continue
            try:
                if int(shot_range[0].split('_')[1]) > int(shot_range[1].split('_')[1]):
                    invalid_input.append(shot_string)
                    continue
            except:pass
            sequence_name = shot_range[0].split('_')[0]
            if sequence_name not in all_sequence:
                invalid_input.append(shot_string)
            else:
                shot_name_range = range(int(shot_range[0].split('_')[1]), int(shot_range[1].split('_')[1])+1)
                shot_names = ["%s_%s" % (sequence_name, str(shot_name).zfill(3))
                              for shot_name in shot_name_range]
                all_shots.extend(shot_names)
        # single shot
        elif re.match(single_pattern, shot_string):
            sequence_name = shot_string.split('_')[0]
            if sequence_name not in all_sequence:
                invalid_input.append(shot_string)
            else:
                all_shots.append(shot_string)
        else:
            invalid_input.append(shot_string)
    if not invalid_input:
        return list(set(all_shots))
    else:
        invalid_string = "Wrong input:\t"
        for invalid_shot_string in invalid_input:
            invalid_string = invalid_string+invalid_shot_string+'\n'
        return invalid_string


if __name__ == "__main__":
    pass
