# -*- coding: utf-8 -*-
from miraPipeline.pipeline.version_up import version_up
reload(version_up)


def main():
    version_up.version_up()


if __name__ == "__main__":
    main()
