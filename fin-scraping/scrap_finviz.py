import sys, os, re
import time
import logging.config
import urllib.request
from html import unescape as unescape     # iPython 3.4+ ==> html.unescape(s)
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from fincore import FinCoremodel, FinCoremodelException


def get_fundametal_data(keys, values, index, default=None):
    try:
        return keys[index].findAll(text=True)[0] + "=" + values[index].findAll(text=True)[0]
    except IndexError:
        return default


def web_scrap(logger, sym_list, base_url, u_a):

    for _SYM_ in sym_list:

        url = base_url + _SYM_

        req = urllib.request.Request (url)
        req.add_header ('User-Agent', u_a)

        # http://stackoverflow.com/questions/12023135/python-3-errorhandling-urllib-requests
        # https://docs.python.org/3.1/howto/urllib2.html
        try:
            with urllib.request.urlopen (req) as response:
                html = response.read()

        except HTTPError as e:
            logger.error("symbol: URL: {}".format(_SYM_, url), exc_info=True)
            logger.error("Errore applicativo: {}".format(e), exc_info=True)
            continue

        except URLError as e:
            logger.error('failed to reach server: {}'.format(e.reason), exc_info=True)
            break

        yield _SYM_, BeautifulSoup(html, "lxml")


def get_fundamentals(logger, document, core, today):

    _SYM_, bsObj = document

    fout   = open(core.out_path + "finviz-" + _SYM_ + "-" + core._FF_ + "-" + today + ".txt", "w")
    table  = bsObj.find("", {"class":"snapshot-table2"})
    keys   = table.findAll(class_="snapshot-td2-cp")
    values = table.findAll(class_="snapshot-td2")

    x = 0 
    data = get_fundametal_data(keys, values, x)
    while data:
        logger.debug('({}) {}'.format(x,data))
        fout.write(data + os.linesep)
        x += 1
        data = get_fundametal_data(keys, values, x)
    fout.close()


def get_ratings(logger, document, core, today):

    _SYM_, bsObj = document

    fout    = open(core.out_path + "finviz-" + _SYM_ + "-" + core._RT_ + "-" + today + ".txt", "w")
    ratings = bsObj.findAll("", {"class":re.compile("fullview-ratings-*")})
    for item in ratings:
        fout.write(item.get_text())
    fout.close()


def get_news(logger, document, core, today):

    _SYM_, bsObj = document

    fout = open(core.out_path + "finviz-" + _SYM_ + "-" + core._NEWS_ + "-" + today + ".txt", "w")
    furl = open(core.out_path + "finviz-" + _SYM_ + "-URL-" + core._NEWS_ + ".txt", "w")

    for row in bsObj.find("table",{"id":"news-table"}).children:
        #fout.write(str(row))
        items = re.search(r'<tr>.+>(.+)</td>.+href="([^"]+)".+>(.+)</a>.+>(.+)</span>', str(row))
        if items:
            fout.write(items.group(1) + '\n')
            fout.write(unescape((items.group(2))) + '\n')
            furl.write(unescape((items.group(2))) + '\n')
            fout.write(unescape((items.group(3))) + '\n')
            fout.write(items.group(4) + '\n')
    fout.close()
    furl.close()


def main():

    try:
        with FinCoremodel() as core:

            logger      = logging.getLogger(__name__)
            today       = time.strftime("%Y%m%d")
            sym_list    = core.getSymbolList()

            logger.info('symbol list: {}'.format(sym_list))

            #finviz_pages = core.web_scrap(finviz)
            #for document in finviz_pages:
            #   finviz.get_fundamentals(document, today)
            #   finviz.get_ratings(document, today)
            #   ...

            web_pages = web_scrap(logger, sym_list, core.base_url, core.u_a)

            for _document in web_pages:

                _SYM_, bsObj = _document

                # FONDAMENTALI

                get_fundamentals(logger, _document, core, today)

                # RATINGS

                get_ratings(logger, _document, core, today)
                
                # NEWS

                get_news(logger, _document, core, today)

                logger.info(_SYM_ + '...finviz scaping is done')

                if core.scan_url_news:
                    logger.info('TBD : scan_url_news')


    except FinCoremodelException as e:
        #logger.error(e)
        print("FinCoremodel EXEPTION: {}".format(e))
        sys.exit()

if __name__ == "__main__":
    main()
