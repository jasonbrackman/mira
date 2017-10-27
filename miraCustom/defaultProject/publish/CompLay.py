# -*- coding: utf-8 -*-
import logging
import nuke
from miraLibs.pipeLibs import pipeFile
from miraLibs.pyLibs import copy


def main():
    args = nuke.rawArgs
    file_name = args[3]
    # copy to publish
    context = pipeFile.PathDetails.parse_path(file_name)
    publish_path = context.publish_path
    copy.copy(file_name, publish_path)
    logging.info("Copy to publish path.")


if __name__ == "__main__":
    main()




