# -*- coding: utf-8 -*-
import pymel.core as pm


def get_all_reference_file():
    all_reference_file = list()
    references = pm.listReferences()
    if references:
        all_reference_file = [ref.path for ref in references]
    return all_reference_file
