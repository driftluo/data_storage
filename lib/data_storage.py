import pandas as pd
from sqlalchemy import create_engine
import pymysql
from logbook import Logger

log = Logger('DataStorage')


class DataStorageBase:
    def __init__(self, database, user, password, port, db, host='localhost'):
        if database == 'mysql':
            self.engine = create_engine(
                '{0}+pymysql://{1}:{2}@{3}:{4}/{5}'.format(database, user, password, host, port, db))
        else:
            self.engine = create_engine('{0}://{1}:{2}@{3}:{4}/{5}'.format(database, user, password, host, port, db))

    def send(self, tablename, data):
        data.to_sql(tablename, con=self.engine, chunksize=1000, if_exists='append')


class ExcelDataStorage(DataStorageBase):
    def __init__(self, conf, datas):
        DataStorageBase.__init__(self, conf['database'].lower(), conf['user'], conf['password'], conf['port'],
                                 conf['db'],
                                 conf['host'])
        self.datas = datas
        self.conf = conf

    def run(self):
        for file in self.datas['excel_data']:
            try:
                self.data = []
                self.analysis(file)
                for tablename, tabledata in self.data:
                    self.send(tablename, tabledata)
                log.debug(file + '导入完成')
            except Exception as e:
                log.error(e)
                log.error(file + '未导入')

    def analysis(self, file, line=0, sheetname=None):
        '''
        Recursively traverse all the sheets of excel and return the DataFrame
        :param file: list, file path
        :param line: int, the start line
        :param sheetname: str, sheetname
        :return: None
        '''
        a = pd.read_excel(file, sheetname=sheetname,
                          header=line)
        for k, v in a.items():
            if (not v.empty) and [column for column in v.columns if str(column).find('Unnamed') != -1]:
                line += 1
                self.analysis(file, line, [k])
            elif not v.empty:
                v = pd.DataFrame(v.values, columns=[str(i).strip() for i in v.columns])
                k = k.strip()
                self.data.append((k, v))
