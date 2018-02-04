import sys, os

config_keys = {
    'GLOBALS':'GLOBALS'

}

_FF_ = 'FUNDAMENTALS'   # fondamentali
_RT_ = 'RATINGS'        # ratings
_NEWS_ = 'NEWS'         # news


def isLocked(config):
    if config['GLOBALS']['locked']=='Yes':
        # in genere se il flag è =yes ci potremmo attendere di trovare un record
        # per es. sul file 'maintenancelog.txt' con una breve descrizione del motivo...
        #
        print("GLOBALS.locked=Yes : il programma non può essere avviato.")
        #
        # ...e quindi stampare a video il contenuto di questo record
        return True

def startup():

    base_dir= os.path.dirname(os.path.realpath(__file__))

    parent_dir = os.path.split(base_dir)[0]

    config_file = parent_dir + '/config.ini'
    config_log  = parent_dir + '/log.ini'

    config = configparser.ConfigParser()
    config.read(config_file)

    if isLocked(config):
        sys.exit()

    u_a      = config['GLOBALS']['user_agent']
    sym_file = config['GLOBALS']['symbol_file']
    out_path = config['GLOBALS']['output_path']
    base_url = config['GLOBALS']['base_url']

    logging.config.fileConfig(config_log)
    logger = logging.getLogger('finviz_scraping')

    logger.info("START: config file is <{}>".format(config_file))
