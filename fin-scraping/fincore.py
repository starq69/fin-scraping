import sys, os
import configparser
import logging.config

class FinCoremodelException(Exception):
    pass

class FinCoremodel(object):

    _FF_ = 'FUNDAMENTALS'   # fondamentali
    _RT_ = 'RATINGS'        # ratings
    _NEWS_ = 'NEWS'         # news

    sym_file = ''
    u_a = ''
    base_url = ''
    out_path = ''
    logger = None
    config_log = ''
    config_file = ''

    stuff = {}

    start = False

    # TODO
    # trasformare in __init__
    # gestione eccezioni : https://stackoverflow.com/questions/20059766/handle-exception-in-init

    def startup(self):

        def isLocked(config):
            if config['GLOBALS']['locked']=='Yes':
                # in genere se il flag è =yes ci potremmo attendere di trovare un record
                # per es. sul file 'maintenancelog.txt' con una breve descrizione del motivo...
                #
                print("GLOBALS.locked=Yes : il programma non può essere avviato.")
                #
                # ...e quindi stampare a video il contenuto di questo record
                return True

        base_dir= os.path.dirname(os.path.realpath(__file__))

        parent_dir = os.path.split(base_dir)[0]

        self.config_file = parent_dir + '/config.ini'
        self.config_log  = parent_dir + '/log.ini'

        config = configparser.ConfigParser()
        config.read(self.config_file)

        if isLocked(config):
            sys.exit()

        self.u_a      = config['GLOBALS']['user_agent']
        self.sym_file = config['GLOBALS']['symbol_file']
        self.out_path = config['GLOBALS']['output_path']
        self.base_url = config['GLOBALS']['base_url']

        logging.config.fileConfig(self.config_log)
        #logger = logging.getLogger('finviz_scraping')
        self.logger = logging.getLogger(__name__)

        self.logger.info("START: config file is <{}>".format(self.config_file))

        #return config_log
        self.start = True
        return self.start

    def getLog(self):
        if not self.start:
            print (__name__ + ' not initialized : call startup()')
            sys.exit()
        return self.config_log

    def getSymbolList(self):
        sym_list = []
        with open(self.sym_file, 'r') as f:
            for line in f:
                line = line.rstrip()
                sym_list.append(line)
                #self.logger.debug(sym_list)
        return sym_list

    def getStuff(self):
        self.stuff['xxx']='xxx'
        return self.stuff['xxx']
