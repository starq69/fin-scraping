################################
#
# TODO:
#   23-08-2017 : sostituire urllib con requests
#
################################

import sys, os
import time
import re
import configparser
import logging.config
import urllib.request
from html import unescape as unescape     # iPython 3.4+ ==> html.unescape(s)
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

import fincore

def get_fundametal_data(keys, values, index, default=None):
    try:
        return keys[index].findAll(text=True)[0] + "=" + values[index].findAll(text=True)[0]
    except IndexError:
        return default

def main():
    '''
    _FF_ = 'FUNDAMENTALS'   # fondamentali
    _RT_ = 'RATINGS'        # ratings
    _NEWS_ = 'NEWS'         # news

    base_dir= os.path.dirname(os.path.realpath(__file__))

    parent_dir = os.path.split(base_dir)[0]

    config_file = parent_dir + '/config.ini'
    config_log  = parent_dir + '/log.ini'

    config = configparser.ConfigParser()
    config.read(config_file)

    if isLocked(config):
        print("GLOBALS.locked=Yes : il programma non verrà eseguito.")
        sys.exit()

    today = time.strftime("%Y%m%d")

    u_a      = config['GLOBALS']['user_agent']
    sym_file = config['GLOBALS']['symbol_file']
    out_path = config['GLOBALS']['output_path']
    base_url = config['GLOBALS']['base_url']

    logging.config.fileConfig(config_log)
    logger = logging.getLogger('finviz_scraping')
    #logger = logging.getLogger()
    logger.info("START: config file is <{}>".format(config_file))
    '''

    fincore.startup()

    sym_list = []

    with open(sym_file, 'r') as f:
        for line in f:
            line = line.rstrip()
            sym_list.append(line)

    logger.info('symbol list: {}'.format(sym_list))

    for _SYM_ in sym_list:

        #url = "http://finviz.com/quote.ashx?t=" + _SYM_
        url = base_url + _SYM_

        req = urllib.request.Request (url)
        req.add_header ('User-Agent', u_a)

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

        fout = open(out_path + "finviz-" + _SYM_ + "-" + _FF_ + "-" + today + ".txt", "w")

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

        fout = open(out_path + "finviz-" + _SYM_ + "-" + _RT_ + "-" + today + ".txt", "w")

        ratings = bsObj.findAll("", {"class":re.compile("fullview-ratings-*")})
        for item in ratings:
            fout.write(item.get_text())

        fout.close()

        # NEWS

        fout = open(out_path + "finviz-" + _SYM_ + "-" + _NEWS_ + "-" + today + ".txt", "w")
        furl = open(out_path + "finviz-" + _SYM_ + "-URL-" + _NEWS_ + ".txt", "w")

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
