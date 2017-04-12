# -*- coding: utf-8 -*-


def get_maya_asset_task_path(tk, task, version=1):
    template_name = 'maya_asset_publish'
    template = tk.templates[template_name]
    tk.create_filesystem_structure("Task", task['id'], engine="tk-maya")
    context = tk.context_from_entity("Task", task['id'])
    fields = context.as_template_fields(template)
    fields['version'] = version
    # -get current task file path
    task_path = template.apply_fields(fields)
    return task_path

if __name__ == "__main__":
    pass
