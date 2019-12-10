from time import time


class Timer:
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, *args, **kwargs):
        self.end = time() - self.start

    def time(self):
        return self.end
