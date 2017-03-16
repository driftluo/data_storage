#-- coding:utf-8 --

import os
import sys
import toml
from logbook import StreamHandler, RotatingFileHandler
from logbook import set_datetime_format
from collections import defaultdict


def find_data(path):
    """
    Get all files in the directory
    :param dir: path
    :return: list
    """
    datas = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if file[file.rfind('.')+1:] in ['xlsx', 'xls']:
                datas['excel_data'].append(os.path.join(dirpath, file))
            elif file[file.rfind('.')+1:] in ['csv']:
                datas['csv_data'].append(os.path.join(dirpath, file))
            elif file[file.rfind('.')+1:].lower() in ['vbo']:
                datas['vbo'].append(os.path.join(dirpath, file))
            else:
                pass
    return datas


def get_conf(conf_file):
    """ configuration file in toml format """
    with open(conf_file, 'r', encoding="utf-8") as conf_h:
        conf = toml.loads(conf_h.read())
    return conf

set_datetime_format('local')

def setup_log(conf):
    """ setup logger for app """
    debug = conf['debug']

    logfile = conf['logfile']
    backup_count = conf['backup_count']
    max_size = conf['max_size']
    format_string = conf['format_string']

    if debug:
        StreamHandler(sys.stdout, format_string=format_string).push_application()
    else:

        full_log_path = os.path.abspath(logfile)
        dir_path = os.path.dirname(full_log_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        RotatingFileHandler(logfile, mode='a', encoding='utf-8',
                            level=0, format_string=format_string, delay=False, max_size=max_size,
                            backup_count=backup_count, filter=None, bubble=True).push_application()