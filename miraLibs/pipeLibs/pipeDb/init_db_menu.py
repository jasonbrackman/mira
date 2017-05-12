from miraLibs.pipeLibs import pipeFile
import task_from_path
from miraLibs.osLibs import get_engine, get_scene_name


def start_engine(tk, path, template_name):
    import sgtk
    try:
        template = tk.templates[template_name]
    except:
        print "No template: %s" % template_name
        return
    is_validate = template.validate(path)
    if is_validate:
        current_task = task_from_path.task_from_path(path)
        context = tk.context_from_entity("Task", current_task["id"])
        try:
            sgtk.platform.current_engine().destroy()
        except:pass
        sgtk.platform.start_engine("tk-maya", tk, context)
        return True


def init_shotgun_menu(project):
    from miraLibs.sgLibs import get_tk_object
    path = get_scene_name.get_scene_name()
    tk = get_tk_object.get_tk_object(project)
    engine = get_engine.get_engine()
    if start_engine(tk, path, "%s_asset_local" % engine):
        return
    if start_engine(tk, path, "%s_asset_work" % engine):
        return
    if start_engine(tk, path, "%s_shot_local" % engine):
        return
    if start_engine(tk, path, "%s_shot_work" % engine):
        return


def init_db_menu(*args):
    from miraLibs.pipeLibs import pipeMira
    path = get_scene_name.get_scene_name()
    obj = pipeFile.PathDetails.parse_path(path)
    if not obj:
        return
    project = obj.project
    database = pipeMira.get_site_value(project, "database")
    if database == "shotgun":
        init_shotgun_menu(project)
