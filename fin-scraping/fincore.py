import sys, os
import configparser
import logging, logging.config

class FinCoremodelException(Exception):
    '''
    original_exception = None

    def __init__(self, msg, original_exception):
        super(FinCoremodelException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
    '''
    pass

class FinCoremodel(object):

    _FF_ = 'FUNDAMENTALS'   # fondamentali
    _RT_ = 'RATINGS'        # ratings
    _NEWS_ = 'NEWS'         # news

    def __init__(self):

        base_dir= os.path.dirname(os.path.realpath(__file__))

        parent_dir = os.path.split(base_dir)[0]

        self.config_file = parent_dir + '/config.ini'
        self.config_log  = parent_dir + '/log.ini'

        self.config = configparser.ConfigParser()


    def __enter__(self):

        if not self.config.read(self.config_file):

            raise FinCoremodelException('missing <' + self.config_file + '> configuration file.')

        elif self.config['GLOBALS']['locked'] == 'Yes':

            raise FinCoremodelException("GLOBALS.locked=Yes : il programma non può essere avviato.")
        else:
            logging.config.fileConfig(self.config_log)
            self.logger = logging.getLogger(__name__)
            self.logger.info('START: config file is <{}>'.format(self.config_file))

            self.u_a = self.config['GLOBALS']['user_agent']
            self.sym_file = self.config['GLOBALS']['symbol_file']
            self.out_path = self.config['GLOBALS']['output_path']
            self.base_url = self.config['GLOBALS']['base_url']

            return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        print("__exit__")

    def getSymbolList(self):
        sym_list = []
        with open(self.sym_file, 'r') as f:
            for line in f:
                line = line.rstrip()
                sym_list.append(line)
                #self.logger.debug(sym_list)
        return sym_list

