import pandas as pd
import shutil
import os
import pathlib


class GoStorage:
    def __init__(self, frame: pd.DataFrame, part=1):
        self._frame = frame
        self._part = part
        self._local = f'{pathlib.Path().resolve().__str__()}/temp'

    def _checkpart(self):
        return self._frame.shape[0]%self._part == 0

    def find_part(self, max, min):
        for i in range(max, min-1, -1):
            if self._frame.shape[0]%i == 0:
                self._size = self._frame.shape[0]/i
                self._part = i
                break
        return self

    def store(self):
        next = 0
        if os.path.exists(self._local):
            self.clear()
            os.makedirs(self._local)
        else:
            os.makedirs(self._local)

        for i in range(self._part):
            self._frame.iloc[:, next:next+next].to_csv(f'{self._local}/{i+1}_tmp.csv', index=False)
            next += self._size
        return self

    def clear(self):
        shutil.rmtree(self._local)