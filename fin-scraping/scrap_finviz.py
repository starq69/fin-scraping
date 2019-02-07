import sys
import time
import logging.config
import urllib.request
from html import unescape as unescape     # iPython 3.4+ ==> html.unescape(s)
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from fincore import FinCoremodel, FinCoremodelException
import finviz


def main():

    try:
        with FinCoremodel() as core:

            logger      = logging.getLogger(__name__)
            today       = time.strftime("%Y%m%d")
            sym_list    = core.getSymbolList()

            logger.info('symbol list: {}'.format(sym_list))

            # AS-IS : finviz è un modulo (senza inizializzazione)
            # TO-BE:  finviz sarà un'istanza di classe inzializzata con ad es. sym_list e con suoi settings come base_url)

            finviz          = core.add_web_scraper('finviz') 
            finviz_pages    = finviz.scraping(sym_list, core.base_url, core.u_a)

            for _document in finviz_pages:

                _SYM_, bsObj = _document

                # FONDAMENTALI

                finviz.get_fundamentals(_document, core, today)

                # RATINGS

                finviz.get_ratings(_document, core, today)
                
                # NEWS

                finviz.get_news(_document, core, today)

                logger.info(_SYM_ + '...finviz scaping is done')

                if core.scan_url_news:
                    logger.info('TBD : scan_url_news')


    except FinCoremodelException as e:
        logger.error(e)
        print("FinCoremodel EXEPTION: {}".format(e))
        sys.exit()

if __name__ == "__main__":
    main()
