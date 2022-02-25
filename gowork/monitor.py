from time import time


class GoTimer:
    def __init__(self, verbose=True):
        self.__verbose = verbose

    def start(self):
        self.start = time()
        self.__total = 0.0
        self.schedule = []
        return self

    def checkpoint(self, reset=True):
        if self.__verbose:
            print(f'{time()-self.start:.1f} sec')
        self.schedule.append(time()-self.start)
        self.__total += time()-self.start
        if reset:
            self.reset()

    def reset(self):
        self.start = time()

    def stop(self, schedule=False):
        if self.__verbose:
            print(f'{time()-self.start:.1f} sec')
        print(f'total time: {self.__total:.1f} sec')
        if schedule:
            print(f'schedule: {self.schedule}')
        self.start = None


def clear_memory(frame, columns=[]):
    if len(columns) == 0:
        columns = frame.columns
    frame.drop(columns, axis=1)
    for column in columns:
        del frame[column]
        del column