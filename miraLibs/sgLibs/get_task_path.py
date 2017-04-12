# -*- coding: utf-8 -*-


def get_task_path(tk, engine, task, template_name, version=1):
    template = tk.templates[template_name]
    tk.create_filesystem_structure("Task", task['id'], engine=engine)
    context = tk.context_from_entity("Task", task['id'])
    fields = context.as_template_fields(template)
    fields['version'] = version
    # -get current task file path
    task_path = template.apply_fields(fields)
    return task_path


if __name__ == "__main__":
    pass
