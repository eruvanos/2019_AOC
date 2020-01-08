from collections import namedtuple
from queue import Queue
from threading import Thread, Lock

from op_machine import Interpreter

Packet = namedtuple('Packet', 'dest x y')


def new_inter(address):
    inter = Interpreter.from_file('input.txt')
    inter.stdin = NetQueue()
    inter.start()
    inter.put(address)
    return inter


class NetQueue(Queue):

    def __init__(self):
        super().__init__()

        self._lock = Lock()

    def get(self, *_):
        with self._lock:
            if self.empty():
                print(f'')
                return -1
            else:
                return super().get(True, None)

    def put(self, *values):
        with self._lock:
            for v in values:
                super().put(v)

def receiver(package_queue: Queue, inter: Interpreter):
    while not inter.finished:
        dest, x, y = inter.get(), inter.get(), inter.get()
        package_queue.put(Packet(dest, x, y))


def solve():
    inters = {i: new_inter(i) for i in range(50)}

    q = Queue()
    for i in inters.values():
        Thread(target=receiver, args=(q, i), daemon=True).start()

    while True:
        dest, x, y = q.get()
        print(f'[{dest}]({x},{y})')

        if dest == 255:
            exit()

        inters[dest].stdin.put(x, y)

if __name__ == '__main__':
    solve()


    # q = Queue()
    #
    # def exint(address):
    #     inter = Interpreter.from_file('input.txt')
    #     inter.stdin = NetQueue()
    #     inter.put(0)
    #     inter.start()
    #     while not inter.finished:
    #         q.put(f'{address} {inter.get()} {inter.get()} {inter.get()}')
    #
    # for i in range(50):
    #     Thread(target=exint, args=(i,)).start()
    #
    # while True:
    #     print(q.get())