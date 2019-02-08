#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import logging.config
from fincore import FinCoremodel, FinCoremodelException
import finviz

#import urllib.request
#from urllib.error import URLError, HTTPError
#from bs4 import BeautifulSoup

def main():

    try:
        with FinCoremodel() as core:

            logger      = logging.getLogger(__name__)
            today       = time.strftime("%Y%m%d")
            sym_list    = core.getSymbolList()

            logger.info('symbol list: {}'.format(sym_list))

            finviz          = core.supply_web_scraper('finviz', kw_arg='starq')
            finviz_pages    = finviz.scraping(sym_list, core.u_a)

            for _document in finviz_pages:

                _SYM_, bsObj = _document

                finviz.load_fundamentals(_document, today)  # fondamentali
                finviz.load_ratings(_document, today)       # ratings
                finviz.load_news(_document, today)          # news

                logger.info('scaping symbol <{}> done'.format(_SYM_))

                if core.scan_url_news:
                    logger.info('TBD : scan_url_news')


    except FinCoremodelException as e:
        logger.error(e)
        sys.exit()

if __name__ == "__main__":
    main()
