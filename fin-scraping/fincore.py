#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import configparser
import logging, logging.config
from utils import supply_instance

#_documents = {}

class FinCoremodelException(Exception):

    original_exception = None

    def __init__(self, msg, original_exception=None):
        super(FinCoremodelException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception


class FinCoremodel(object):

    _FF_    = 'FUNDAMENTALS'   # fondamentali
    _RT_    = 'RATINGS'        # ratings
    _NEWS_  = 'NEWS'         # news

    def __init__(self):

        base_dir    = os.path.dirname(os.path.realpath(__file__))
        parent_dir  = os.path.split(base_dir)[0]

        self.config_file = parent_dir + '/config.ini'
        self.config_log  = parent_dir + '/log.ini'
        self.config      = configparser.ConfigParser()

        self._scrapers   = dict() ### scraper instances


    def __enter__(self):

        try:
            if not self.config.read(self.config_file):

                raise FinCoremodelException('missing <' + self.config_file + '> configuration file.')

            elif self.config['GLOBALS']['locked'] == 'Yes':

                raise FinCoremodelException(__name__ + ' is locked. To run it unset GLOBALS.locked')
            else:
                logging.config.fileConfig(self.config_log)
                self.log = logging.getLogger(__name__)

                self.u_a      = self.config['GLOBALS']['user_agent']
                self.sym_file = self.config['GLOBALS']['symbol_file']
                self.out_path = self.config['GLOBALS']['output_path']
                self.base_url = self.config['GLOBALS']['base_url']
                self.scan_url_news = self.config['GLOBALS']['scan_url_news']

                self.log.info('START: config file is <{}>'.format(self.config_file))
                if self.scan_url_news:
                    self.log.info('scan_url_news flag is FALSE') ##!!

                return self

        except configparser.Error as e:
            self.log.error ('configparser.Error : {} --> ABORT'.format (e))
            sys.exit(1)

        except Exception as e:
            '''
            if self.__exit__(*sys.exc_info()):
                self.enter_ok = False
            else:
                raise
            '''
            self.__exit__(*sys.exc_info()) ##TODO
            raise e


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


    def getSymbolList(self):
        sym_list = []
        with open(self.sym_file, 'r') as f:
            for line in f:
                line = line.rstrip()
                sym_list.append(line)
                #self.log.debug(sym_list)
        return sym_list


    def add_web_scraper(self, ws_name):
        module = ws_name.strip()
        self.log.debug('try to import module <{}>'.format(module))
        if module not in self._scrapers:
            try:
                self._scrapers[module] = importModule(module)  
                self.log.info('==> model <{}> loaded'.format(module))
                return self._scrapers[module]

            except Exception as e:
                self.log.error('fail to load model {} : ABORT'.format(module, e))
                raise e
                #sys.exit(1)
        else:
                self.log.info('==> model <{}> already loaded'.format(module))
                return self._scrapers[module]


    def supply_web_scraper(self, ws_name, **kwargs):

        _instance = ws_name.strip()
        if _instance not in self._scrapers:
            try:
                self._scrapers[_instance] = supply_instance(_instance, **kwargs)  
                self.log.info('web-scraper <{}> instance succesfully created'.format(_instance))
                return self._scrapers[_instance]

            except Exception as e:
                #self.log.error('FAIL to create web-scraper <{}> instance: ABORT'.format(_instance))
                raise FinCoremodelException('FAIL to create web-scraper <{}> instance: ABORT'.format(_instance), e)
                #sys.exit(1)
        else:
                self.log.info('web-scraper <{}> instance already created '.format(_instance))
                return self._scrapers[_instance]
