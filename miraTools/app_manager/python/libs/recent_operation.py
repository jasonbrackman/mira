# -*- coding: utf-8 -*-
from . import get_conf_path
from . import conf_parser


recent_conf_path = get_conf_path.get_conf_path("recent_app.yml")
cp = conf_parser.ConfParser(recent_conf_path)
current_conf_data = cp.parse().get()


def save_to_recent(name, exe_path):
    if current_conf_data:
        recent_app_list = current_conf_data["recent_apps"]
        recent_app_names = [key for i in recent_app_list for key in i]
        # if exist in recent, make it the first one
        if name in recent_app_names:
            if recent_app_names[0] == name:
                return
            name_index = recent_app_names.index(name)
            current_app = recent_app_list.pop(name_index)
            recent_app_list.insert(0, current_app)
        # if not in, add it.
        else:
            if len(recent_app_list) == 5:
                recent_app_list.pop(-1)
            recent_app_list.insert(0, {name: exe_path})
        new_data = {"recent_apps": recent_app_list}
    else:
        new_data = {"recent_apps": [{name: exe_path}]}
    cp.parse().set(new_data)


def remove_from_recent(name):
    if current_conf_data:
        recent_app_list = current_conf_data["recent_apps"]
        for app_dict in recent_app_list:
            for key in app_dict:
                if key == name:
                    recent_app_list.remove(app_dict)
        new_data = {"recent_apps": recent_app_list}
        cp.parse().set(new_data)
