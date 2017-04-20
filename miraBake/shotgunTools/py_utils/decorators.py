#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :heshuai
# mtine       :2015/12/3
# version     :
# usage       :
# notes       :

# Built-in modules
import logging
# Third-party modules

# Studio modules

# Local modules


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def debugger(func):
    def _wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logger.debug('Run successful [file]:%s [func]:%s' % (__file__, func.__module__))
        except Exception, e:
            logger.error('Run failed [file]:%s [func]:%s' % (__file__, func.__module__))
            logger.error(e)
    return _wrapper
