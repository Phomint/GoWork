from safe.configs import Credentials
from pyathena import connect
from pyathena.pandas.util import as_pandas
from sqlalchemy import create_engine
import pandas as pd
from pyspark.sql import SparkSession
from pyspark import pandas as pds
import glob
import pathlib


class AthenaGo:
    def __init__(self):
        self._cred = Credentials().select('Athena', 'datalake')
        self._con = connect(s3_staging_dir=self._cred['s3_staging_dir'],
                            region_name=self._cred['region_name'])
        self._cursor = self._con.cursor()

    def read_sql(self, sql, verbose=False):
        if verbose:
            print(sql)
        return as_pandas(self._cursor.execute(sql))


class GoSpark:
    def __init__(self, host='local'):
        self.spark_session = SparkSession.builder.master(host).getOrCreate()
        self.pandas = pds


class MysqlGo:
    def __init__(self, base):
        self._buildurl(base)
        self._engine()
        self._pandas = pd

    def _buildurl(self, base):
        self._cred = Credentials().select('MySQL', base)
        self.url = f'mysql+pymysql://{self._cred["user"]}:{self._cred["password"]}@{self._cred["host"]}:{self._cred["port"]}/{self._cred["database"]}'

    def _engine(self):
        self._engine = create_engine(self.url)

    def spark(self):
        spark = GoSpark()
        self.spark_session = spark.spark_session
        self._pandas = spark.pandas
        return self

    def read_sql(self, sql):
        return self._pandas.read_sql(sql, con=self._engine)


class GoQuery:
    """This object load sql files and insert them into a dictionary to access via their key,
        which receives the same name as the file
    """
    def __init__(self, path: str):
        """
        :param path: Where your sql files are located
        """
        self.queries = {}
        self.path = path
        self._root = pathlib.Path().resolve().__str__()
        self._loadfiles()

    def _loadfiles(self):
        """
        Internal method that go through all files in directory and insert into a dictionary
        :return: None
        """
        for path in glob.glob(f"{self._root + '/' + self.path}/*.sql"):
            self._cachefile(path.split('/')[-1])

    def _cachefile(self, file: str):
        """
        Insert into dictionary
        :param file: File name
        :return: None
        """
        with open(self._root + '/' + self.path + '/' + file, 'r', encoding='utf-8') as line:
            self.queries[file.replace('.sql', '')] = line.read()
