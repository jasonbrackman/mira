# -*- coding: utf-8 -*-

    
def get_task_type_engine(task_type):
    if task_type == "art":
        return "photoshop"
    return "maya"
        

class PublishPathCalculator(object):
    
    def __init__(self, tk):
        self.tk = tk
        self.sg = self.tk.shotgun

    def _get_task_id(self, entity, task_type):
        filters = [["entity","name_is",entity],["sg_task_type", "name_is", task_type]]
        current_task = self.sg.find_one("Task",filters)
        if not current_task:
            return
        task_id  = current_task["id"]
        return task_id
        
    def _calculat_file_path(self, task_id, engine, entity_type):
        template = self.tk.templates["{engine}_{entity_type}_publish".format(engine=engine, entity_type=entity_type)]
        # create folders for this entity
        #print self.tk.preview_filesystem_structure("Task", task_id)[5]
        self.tk.create_filesystem_structure("Task", task_id, engine="tk-%s" % engine)
        ctx = self.tk.context_from_entity("Task", task_id)
        fields = ctx.as_template_fields(template)
        fields["version"] = 0
        return template.apply_fields(fields)
    
    def calculat(self, entity_name, task_type):
        task_id = self._get_task_id(entity_name, task_type)
        if not task_id:
            raise ValueError("No task muchs condition %s,%s." % (entity_name, task_type))
        engine = get_task_type_engine(task_type)
        is_shot = "_" in entity_name            #  Only shot have a "_" in it.
        if is_shot:
            entity_type = "shot"
        else:
            entity_type = "asset"
        return self._calculat_file_path(task_id, engine, entity_type)

if __name__ == "__main__":
    from get_tk_object import get_tk_object
    tk = get_tk_object()
    path_calculator = PublishPathCalculator(tk)
    print path_calculator.calculat("YoungDouFu", "mdl")
    print path_calculator.calculat("999_000","pv")
