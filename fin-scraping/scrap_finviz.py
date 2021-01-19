#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import logging
#import logging.config
from fincore import FinCoremodel, FinCoremodelException
#import finviz

#import urllib.request
#from urllib.error import URLError, HTTPError
#from bs4 import BeautifulSoup

def main():

    try:
        # TODO passare un TAG ? (gestire sulla Fincormodel.__init__(...)
        with FinCoremodel() as core:

            logger      = logging.getLogger(__name__)
            today       = time.strftime("%Y%m%d")

            # NB: ottenere prima finviz via core.supply_web_scraper() e poi finviz.getSymbolList() ora erronemanete in core (FinCoremodel)

            # TODO dopo finviz=core... come metodo di finviz e non di core?
            sym_list    = core.getSymbolList()
            logger.info('symbol list: {}'.format(sym_list))

            finviz          = core.supply_web_scraper('finviz', config_file=core.config_file)
            finviz_pages    = finviz.scraping(sym_list) 

            for _document in finviz_pages:

                _SYM_, bsObj = _document
                logger.info(type(bsObj)) # <class 'bs4.BeautifulSoup'> 

                #'''starq@2021:debug
                finviz.load_fundamentals(_document, today)  # fondamentali
                finviz.load_ratings(_document, today)       # ratings
                finviz.load_news(_document, today)          # news
                #'''
                logger.info('scaping symbol <{}> done'.format(_SYM_))

                if core.scan_url_news:
                    logger.info('TBD : scan_url_news')


    except FinCoremodelException as e:
        logger.error(e)
        sys.exit()

if __name__ == "__main__":
    main()
