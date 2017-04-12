# -*- coding: utf-8 -*-
import pymel.core as pm


def get_asset_names(include_env=True):
    asset_names = list()
    transforms = pm.ls(type="transform")
    for transform in transforms:
        if not transform.endswith("_MODEL"):
            continue
        if include_env:
            asset_names.append(transform)
        else:
            no_namespace_name = transform.split(":")[-1]
            if not no_namespace_name.startswith("env_"):
                asset_names.append(transform)
    return asset_names


if __name__ == "__main__":
    pass
