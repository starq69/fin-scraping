#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import configparser
import logging, logging.config
from fincore import FinCoremodelException


class WebScraper(object):

    def __init__(self, **kwargs):

        base_dir    = os.path.dirname (os.path.realpath(__file__))
        parent_dir  = os.path.split (base_dir)[0] + '/'
        config_file = parent_dir + self.__class__.__name__+'.ini'
        config      = configparser.ConfigParser()
        self.log    = logging.getLogger(__name__)
        self.log.info(kwargs) ##

        try:
            if not config.read(config_file):
                raise FinCoremodelException('missing <' + config_file + '> configuration file.')
            else:
                ## TODO gestire user_agents come indicato su fincore.py 
                #self.u_a      = self.config['GLOBALS']['user_agent']
                self.out_path = config['GLOBALS']['output_path']
                self.base_url = config['GLOBALS']['base_url']

        except configparser.Error as e:
            self.log.error ('configparser.Error : {} '.format(repr(e)))
            raise
            #sys.exit(1)
        except Exception as e:
            self.log.error(repr(e))
            raise


    def delivering(self, key=None, doc=None):

        self.auto_throttling()
        return key, doc


    def auto_throttling(self):

        ##TODO 
        '''https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/'''
        self.log.info('auto-throttling not yet implemented ;)')
