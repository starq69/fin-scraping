#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
https://stackoverflow.com/questions/301134/dynamic-module-import-in-python
https://stamat.wordpress.com/2013/06/30/dynamic-module-import-in-python/
'''
import sys, logging
#import imp          ## deprecated from 3.4
import importlib


def supply_instance(name, **kwargs):

    log     = logging.getLogger(__name__)
    name    = name.strip()
    _class  = name[0].upper() + name[1:]
    try:
        module = __import__(name)
        _class = getattr(module, _class)
        return _class(**kwargs)

    except Exception as e:
        log.error(repr(e)) 
        log.exception(e)
        raise e 
