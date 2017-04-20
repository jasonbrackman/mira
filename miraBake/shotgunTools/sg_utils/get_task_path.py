#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/12/21
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules

# Studio modules

# Local modules


def get_task_path(tk, template_name, engine, task):
    template = tk.templates[template_name]
    tk.create_filesystem_structure("Task", task['id'], engine=engine)
    context = tk.context_from_entity('Task', task['id'])
    fields = context.as_template_fields(template)
    fields['version'] = 1
    task_path = template.apply_fields(fields)
    return task_path
