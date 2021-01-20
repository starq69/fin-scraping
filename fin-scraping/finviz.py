#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re
import logging
from bs4 import BeautifulSoup 
import urllib.request
from html import unescape as unescape     # iPython 3.4+ ==> html.unescape(s)
from urllib.error import URLError, HTTPError
from webscraper import WebScraper

'''
    modulo plug-in 
    filename : <name>.py
    classe   : <Name>(WebScraper)
'''
class Finviz(WebScraper):

    def __init__(self, **kwargs):

        super().__init__(**kwargs) 
        self.log = logging.getLogger(__name__)
        self.log.info("Finviz.__init__()")


    def scraping(self, sym_list): 
        '''TODO
        (self, sym_list=None, ...
        n.b. se sym_list == None usa core.getSymbolList()
        '''
        for _SYM_ in sym_list:

            url = self.base_url + _SYM_ 

            # TODO rimuovere u_a dalla config. ed utilizzare ad es. random.choice(ua_list) con user_agent.generate_user_agent() 
            # vedere: https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
            req = urllib.request.Request (url)
            req.add_header ('User-Agent', self.u_a)

            # http://stackoverflow.com/questions/12023135/python-3-errorhandling-urllib-requests
            # https://docs.python.org/3.1/howto/urllib2.html
            try:
                with urllib.request.urlopen (req) as response:
                    html = response.read()

            except HTTPError as e:
                self.log.error("symbol: URL: {}".format(_SYM_, url), exc_info=True)
                self.log.error("Errore applicativo: {}".format(e), exc_info=True)
                continue

            except URLError as e:
                self.log.error('failed to reach server: {}'.format(e.reason), exc_info=True)
                break

            yield self.delivering(key=_SYM_, doc=BeautifulSoup(html, "lxml"))


    def load_fundamentals(self, document, today):

        def get_fundametal_data(keys, values, index, default=None):
            try:
                return keys[index].findAll(text=True)[0] + "=" + values[index].findAll(text=True)[0]
            except IndexError:
                return default


        _SYM_, bsObj = document
        _FF_ = 'FUNDAMENTALS' ##TODO

        table  = bsObj.find("", {"class":"snapshot-table2"})
        # starq@2021: table is None!
        if table is not None:
            fout   = open(self.out_path + "finviz-" + _SYM_ + "-" + _FF_ + "-" + today + ".txt", "w")
            keys   = table.findAll(class_="snapshot-td2-cp")
            values = table.findAll(class_="snapshot-td2")
            x = 0 
            data = get_fundametal_data(keys, values, x)
            while data:
                self.log.debug('({}) {}'.format(x,data))
                fout.write(data + os.linesep)
                x += 1
                data = get_fundametal_data(keys, values, x)
            fout.close()
        else:
            self.log.error("bsObj.find(\"\", {\"class\":\"snapshot-table2\"}) non ha trovato nulla!")


    def load_ratings(self, document, today):

        _SYM_, bsObj = document
        _RT_ = 'RATINGS' ##TODO
        ratings = bsObj.findAll("", {"class":re.compile("fullview-ratings-*")})
        if ratings is not None:
            self.log.info("file <"+self.out_path + "finviz-" + _SYM_ + "-" + _RT_ + "-" + today + ".txt"+">")
            fout    = open(self.out_path + "finviz-" + _SYM_ + "-" + _RT_ + "-" + today + ".txt", "w")
            for item in ratings:
                fout.write(item.get_text())
            fout.close()
        else:
            self.log.error("no rating entry found!")


    def load_news(self, document, today):

        _SYM_, bsObj = document
        _NEWS_ = 'NEWS' ##TODO

        fout = open(self.out_path + "finviz-" + _SYM_ + "-" + _NEWS_ + "-" + today + ".txt", "w")
        furl = open(self.out_path + "finviz-" + _SYM_ + "-URL-" + _NEWS_ + ".txt", "w")

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
