import pandas as pd
import shutil
import os
import pathlib


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

    def clear(self):
        shutil.rmtree(self.__local)