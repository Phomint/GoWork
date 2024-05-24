import pandas as pd
import shutil
import os
import pathlib
import platform
import glob


class GoStorage:
    def __init__(self, frame: pd.DataFrame, part=1):
        self.__frame = frame
        self.__part = part
        self.__local = f'{pathlib.Path().resolve().__str__()}/temp'

    def __checkpart(self):
        return self.__frame.shape[0]%self.__part == 0

    def find_part(self, max, min):
        for i in range(max, min-1, -1):
            if self.__frame.shape[0]%i == 0:
                self.__size = self.__frame.shape[0]/i
                self.__part = i
                break
        return self

    def store(self):
        next = 0
        if os.path.exists(self.__local):
            self.clear()
            os.makedirs(self.__local)
        else:
            os.makedirs(self.__local)

        for i in range(self.__part):
            self.__frame.iloc[:, next:next+next].to_csv(f'{self.__local}/{i+1}_tmp.csv', index=False)
            next += self.__size
        return self


class Files:

    def __init__(self, path: str, type='csv'):
        self.__platform = '\\' if platform.system().__str__() == 'Windows' else '/'
        self.__frames = {}
        self.path = path
        self.__root = pathlib.Path().resolve().__str__()
        self.__type = type
        self.__loadfiles()

    def use(self, frame_name: str):
        return self.__frames[frame_name]

    def use_index(self, index: int):
        return self.__frames[list(self.__frames.keys())[index]]

    def __loadfiles(self):
        for path in glob.glob(f"{self.__root + self.__platform + self.path + self.__platform}*.{self.__type}"):
            self.__cachefile(path.split(self.__platform)[-1])

    def __cachefile(self, file: str):
        """
        Insert into dictionary
        :param file: File name
        :return: None
        """
        if self.__type == 'csv':
            result = pd.read_csv(self.__root + self.__platform + self.path + self.__platform + file)
        else:
            result = self.__root + self.__platform + self.path + self.__platform + file

        self.__frames[file.replace(f'.{self.__type}', '')] = result
    def clear(self):
        shutil.rmtree(self.__local)