################################
#
# TODO:
#   23-08-2017 : sostituire urllib con requests
#
################################

import sys, os
import time
import re
#import configparser
import logging.config
import urllib.request
from html import unescape as unescape     # iPython 3.4+ ==> html.unescape(s)
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

from fincore import FinCoremodel

def get_fundametal_data(keys, values, index, default=None):
    try:
        return keys[index].findAll(text=True)[0] + "=" + values[index].findAll(text=True)[0]
    except IndexError:
        return default

def main():

    #fincore.FinCoremodel.startup()

    core = FinCoremodel()

    if not core.startup():
        exit()

    log=core.getLog()

    #log = core.startup()
    logging.config.fileConfig(log)
    logger = logging.getLogger(__name__)

    today = time.strftime("%Y%m%d")

    #sym_list = []

    '''
    https://stackoverflow.com/questions/1971240/python-seek-on-remote-file-using-http
    considerare la possibilità di un sym_file remoto
    url = "http://www.website.com/data/simbol_list.txt"
    r = requests.get(url)
    # If a 4XX client error or a 5XX server error is encountered, we raise it.
    r.raise_for_status()
    '''
    sym_list = core.getSymbolList()

    #stuff = core.getStuff()
    #logger.info('stuff: {}'.format(stuff))

    logger.info('symbol list: {}'.format(sym_list))

    for _SYM_ in sym_list:

        #url = "http://finviz.com/quote.ashx?t=" + _SYM_
        url = core.base_url + _SYM_

        req = urllib.request.Request (url)
        req.add_header ('User-Agent', core.u_a)

        # http://stackoverflow.com/questions/12023135/python-3-errorhandling-urllib-requests
        # https://docs.python.org/3.1/howto/urllib2.html
        try:
            with urllib.request.urlopen (req) as response:
                html = response.read()

        except HTTPError as e:
            logger.error("symbol: URL: {}".format(_SYM_, url))
            logger.error("Errore applicativo: {}".format(e))
            continue

        except URLError as e:
            logger.error('failed to reach server: {}'.format(e.reason))
            break

        bsObj = BeautifulSoup(html, "lxml")

        # FONDAMENTALI

        fout = open(core.out_path + "finviz-" + _SYM_ + "-" + core._FF_ + "-" + today + ".txt", "w")

        table = bsObj.find("", {"class":"snapshot-table2"})

        keys   = table.findAll(class_="snapshot-td2-cp")
        values = table.findAll(class_="snapshot-td2")
        x = 0
        data = get_fundametal_data(keys, values, x)
        while data:
            logger.debug('({}) {}'.format(x,data))
            fout.write(data + os.linesep)
            x += 1
            data = get_fundametal_data(keys, values, x)

        # RATINGS

        fout = open(core.out_path + "finviz-" + _SYM_ + "-" + core._RT_ + "-" + today + ".txt", "w")

        ratings = bsObj.findAll("", {"class":re.compile("fullview-ratings-*")})
        for item in ratings:
            fout.write(item.get_text())

        fout.close()

        # NEWS

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



        logger.info(_SYM_ + '...done')

    sys.exit()

if __name__ == "__main__":
    main()
