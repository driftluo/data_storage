from lib.utils import get_conf
from lib.utils import setup_log
from lib.utils import find_data
from lib.data_storage import ExcelDataStorage

from logbook import Logger
import os

log = Logger('main')

def main():
    conf_file = os.path.join(os.getcwd(), 'conf\data.toml')
    conf = get_conf(conf_file)
    setup_log(conf['logging'])
    log.debug('start...')
    setup(conf)

def setup(conf):
    log.debug('init...')
    datas = find_data(conf['data']['address'])
    worker = ExcelDataStorage(conf['database'], datas)
    worker.run()