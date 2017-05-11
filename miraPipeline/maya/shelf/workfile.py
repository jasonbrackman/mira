# -*- coding: utf-8 -*-
from miraPipeline.pipeline.task_get import task_get
reload(task_get)


def main():
    task_get.run_maya()


if __name__ == "__main__":
    pass
