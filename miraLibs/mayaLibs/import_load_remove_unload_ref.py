# -*- coding: utf-8 -*-
import ReferenceUtility


def import_load_remove_unload_ref():
    ru = ReferenceUtility.ReferenceUtility()
    ru.import_loaded_ref()
    ru.remove_unload_ref()
