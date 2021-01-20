#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
https://stackoverflow.com/questions/301134/dynamic-module-import-in-python
https://stamat.wordpress.com/2013/06/30/dynamic-module-import-in-python/
'''
import sys
from importlib import import_module
import logging
#import importlib


def supply_instance(name, **kwargs):

    log     = logging.getLogger(__name__)
    name    = name.strip()
    _class  = name[0].upper() + name[1:]
    try:
        #module = __import__(name)
        module = import_module(name)
        _class = getattr(module, _class)
        return _class(**kwargs)

    #except Exception as e:
    except (ModuleNotFoundError, AttributeError) as e:
        log.error(repr(e)) 
        log.exception(e)
        raise e 

