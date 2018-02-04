import sys, os
import configparser
import logging.config


class FinCoremodel(object):

    _FF_ = 'FUNDAMENTALS'   # fondamentali
    _RT_ = 'RATINGS'        # ratings
    _NEWS_ = 'NEWS'         # news

    sym_file = ''
    u_a = ''
    base_url = ''
    out_path = ''

    #@staticmethod
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

        config_file = parent_dir + '/config.ini'
        config_log  = parent_dir + '/log.ini'

        config = configparser.ConfigParser()
        config.read(config_file)

        if isLocked(config):
            sys.exit()

        self.u_a      = config['GLOBALS']['user_agent']
        self.sym_file = config['GLOBALS']['symbol_file']
        self.out_path = config['GLOBALS']['output_path']
        self.base_url = config['GLOBALS']['base_url']

        logging.config.fileConfig(config_log)
        #logger = logging.getLogger('finviz_scraping')
        logger = logging.getLogger(__name__)

        logger.info("START: config file is <{}>".format(config_file))

        return config_log
