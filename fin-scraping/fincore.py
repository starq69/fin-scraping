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
        super().__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception


class FinCoremodel(object):

    _FF_    = 'FUNDAMENTALS'   # fondamentali
    _RT_    = 'RATINGS'        # ratings
    _NEWS_  = 'NEWS'         # news

    def __init__(self, **kwargs):

        self._scrapers   = dict() 

        base_dir    = os.path.dirname(os.path.realpath(__file__))
        parent_dir  = os.path.split(base_dir)[0]

        self.config_file = parent_dir + '/config.ini'
        self.config_log  = parent_dir + '/log.ini'
        self.config      = configparser.ConfigParser()

        try:
            if not self.config.read(self.config_file):
                print('EXCEPTION: ('++')missing or invalid configuration file :<' + self.config_file + '> : ABORT')
                sys.exit(1)
                #raise FinCoremodelException('missing or invalid configuration file :<' + self.config_file + '>')

            elif self.config['GLOBALS']['locked'] == 'Yes':
                #raise FinCoremodelException(__name__ + ' is locked. To run it unset GLOBALS.locked')
                print(__name__ + ' is locked. To run it unset GLOBALS.locked : ABORT')
                sys.exit(1)
            else:
                logging.config.fileConfig(self.config_log)
                self.log = logging.getLogger(__name__)
                self.log.info('program started')

            self.web_scraper = kwargs['web_scraper'] ## can raise KeyError

            if type(self.web_scraper) is list:
                self.log.info('<web_scraper> kwarg paramenter need to be a string, list is not yet implemented.')
                sys.exit(1)
            elif type(self.web_scraper) is str:
                self.web_scraper = self.web_scraper.strip()
            else:
                self.log.error('FinCoremodel <web_scraper> paramenter cannot be of type {}'.format(type(self.web_scraper)))
                sys.exit(1)

            self.sym_file = self.config['GLOBALS']['symbol_file']
            self.scan_url_news = self.config['GLOBALS']['scan_url_news'] # flag

            self.log.info('START: config file is <{}>'.format(self.config_file))
            if self.scan_url_news:
                self.log.info('scan_url_news flag is FALSE') ##!!

        except configparser.Error as e:
            self.log.error ('configparser.Error : {} --> ABORT'.format (e))
            sys.exit(1)
        except KeyError as e:
            self.log.error('During inizialization of class FinCoremodel: missing <web_scraper> kwarg: ABORT')
            sys.exit(1)
        except Exception as e:
            
            #if self.__exit__(*sys.exc_info()):
            #    self.enter_ok = False
            #else:
            #    raise

            self.__exit__(*sys.exc_info()) ##TODO
            raise e


    def __enter__(self, **kwargs):

        try:
            self._scrapers[self.web_scraper] = supply_instance(self.web_scraper, config_file=self.config_file)
            self.log.info('web-scraper <{}> instance succesfully created'.format(self.web_scraper))

        except Exception as e:
            #raise FinCoremodelException('FAIL to create web-scraper <{}> instance: ABORT'.format(self.web_scraper), e)
            self.log.error('FAIL to create web-scraper <{}> instance: ABORT'.format(self.web_scraper))
            sys.exit(1)

        return self


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


    def get_web_scraper(self, name):

        if name not in self._scrapers:
            raise FinCoremodelException('The module <{}> is missing from the dynamic modules imported with FinCoremodel'.format(name))

        return self._scrapers[name]
