from gowork.safe.configs import Credentials
from pyathena import connect
from pyathena.pandas.util import as_pandas
from sqlalchemy import create_engine
import pandas as pd
import glob
import pathlib
import base64

class AthenaGo:
    def __init__(self, name_connection: str):
        self.__decode(name_connection)
        self.__con = connect(s3_staging_dir=self.__cred['s3_staging_dir'],
                            region_name=self.__cred['region_name'])
        self.__cursor = self.__con.cursor()

    def read_sql(self, sql, verbose=False):
        if verbose:
            print(sql)
        return as_pandas(self.__cursor.execute(sql))

    def __decode(self, name: str):
        cred = Credentials().select('Athena', name)
        for k, d in cred.items():
            if type(d) == dict:
                cred[k] = base64.b64decode(d['encode'].encode('utf-8')).decode('utf-8')
        self.__cred = cred


class MysqlGo:
    def __init__(self, name_connection: str):
        self.__buildurl(name_connection)
        self.__engine()
        self.__pandas = pd

    def __buildurl(self, name):
        self.__decode(name)
        self.url = f'mysql+pymysql://{self.__cred["user"]}:{self.__cred["password"]}@{self.__cred["host"]}:{self.__cred["port"]}/{self.__cred["database"]}'

    def __engine(self):
        self.__engine = create_engine(self.url)

    def read_sql(self, sql):
        return self.__pandas.read_sql(sql, con=self.__engine)

    def __decode(self, name: str):
        cred = Credentials().select('MySQL', name)
        for k, d in cred.items():
            if type(d) == dict:
                cred[k] = base64.b64decode(d['encode'].encode('utf-8')).decode('utf-8')
        self.__cred = cred

class GoQuery:
    """This object load sql files and insert them into a dictionary to access via their key,
        which receives the same name as the file
    """
    def __init__(self, path: str):
        """
        :param path: Where your sql files are located
        """
        self.__queries = {}
        self.path = path
        self.__root = pathlib.Path().resolve().__str__()
        self.__loadfiles()

    def use(self, query_name: str):
        """Select which query do you want use
        :param query_name: SQL file saved, without extension .sql
        """
        return self.__queries[query_name]

    def __percsign(self, query):
        """By default python uses %% to indicate use of %, so to handle with
        :param query: Any query type string
        """
        return query.replace('%%','%').replace('%','%%')

    def __loadfiles(self):
        """
        Internal method that go through all files in directory and insert into a dictionary
        :return: None
        """
        for path in glob.glob(f"{self.__root + '/' + self.path}/*.sql"):
            self.__cachefile(path.split('/')[-1])

    def __cachefile(self, file: str):
        """
        Insert into dictionary
        :param file: File name
        :return: None
        """
        with open(self.__root + '/' + self.path + '/' + file, 'r', encoding='utf-8') as line:
            self.__queries[file.replace('.sql', '')] = self.__percsign(line.read())
