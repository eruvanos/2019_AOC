from collections import namedtuple
from queue import Queue, Empty
from threading import Thread, Lock
from time import sleep

from op_machine import Interpreter

Packet = namedtuple('Packet', 'dest x y')


def new_inter(address):
    inter = Interpreter.from_file('input.txt')
    inter.stdin = NetQueue()
    # inter.DEBUG = True
    inter._log_prefix = str(address)

    inter.put(address)
    inter.start()
    return inter


class NAS(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.x = None
        self.y = None

    def put(self, x, y):
        print(f'NAS Update:', x, y)
        self.x = x
        self.y = y


class NetQueue(Queue):
    def __init__(self):
        super().__init__()

        self._lock = Lock()
        self._blocked = 0

    def get(self, *_):
        with self._lock:
            try:
                return super().get(True, 0.1)
            except Empty:
                self._blocked += 1
                return -1

    def put(self, *values):
        with self._lock:
            self._blocked = 0
            for v in values:
                super().put(v)

    @property
    def blocked(self):
        return self._blocked > 2


def receiver(package_queue: Queue, inter: Interpreter):
    while not inter.finished:
        dest, x, y = inter.get(), inter.get(), inter.get()
        package_queue.put(Packet(dest, x, y))


def all_idle(inters):
    for i in range(50):
        if not inters[i].stdin.blocked:
            return False
    return True


def solve():
    print('Start interpreters')
    inters = {i: new_inter(i) for i in range(50)}

    q = Queue()
    print('Start receivers interpreters')
    for i in inters.values():
        Thread(target=receiver, args=(q, i), daemon=True).start()

    print('Create NAS')
    nas = NAS()
    history = set()

    print('Start handle packages')
    while True:
        while q.empty():
            print('empty queue wait for interpreters')

            if all_idle(inters):
                print(f'send NAS package {len(history)}')
                if (nas.x, nas.y) in history:
                    print(f'Second package with', nas.x, nas.y)
                    exit()
                q.put(Packet(0, nas.x, nas.y))
                history.add((nas.x, nas.y))
            sleep(1)

        dest, x, y = q.get()
        print(f'[{dest}]({x},{y})')

        if dest == 255:
            nas.put(x, y)
        else:
            inters[dest].stdin.put(x, y)


if __name__ == '__main__':
    solve()
