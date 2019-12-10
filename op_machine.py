from collections import defaultdict
from queue import Queue
from threading import Thread
from typing import List, Tuple, Dict, Union


def read_input(_list: list):
    return {i: int(v) for i, v in enumerate(_list)}


# class Ref(int):
#     pass

class Param:
    def set(self, value):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()

    def __call__(self, *args):
        if len(args) == 1:
            self.set(args[0])
        else:
            return self.get()


class Ref(Param):
    def __init__(self, interpreter, value):
        self._interpreter = interpreter
        self._value = value

    def set(self, value):
        self._interpreter[self._value] = value

    def get(self):
        return self._interpreter[self._value]

    def __repr__(self):
        return f'Ref[{self._value}]->{self()}'


class Rel(Param):
    def __init__(self, interpreter: 'Interpreter', value):
        self._interpreter = interpreter
        self._value = value

    def set(self, value):
        self._interpreter[self._value + self._interpreter._rbo] = value

    def get(self):
        return self._interpreter[self._value + self._interpreter._rbo]

    def __repr__(self):
        return f'Rel[{self._value}]->{self()}'


class Var(Param):
    def __init__(self, value):
        self._value = value

    def set(self, value):
        raise Exception('Writing to a Var is permitted')

    def get(self):
        return self._value

    def __repr__(self):
        return f'Var->{self()}'


class Interpreter:
    DEBUG = False

    def __init__(self, programm: List[int]) -> None:
        super().__init__()
        self._memory: Dict[int, int] = defaultdict(
            default_factory=int,
            **{k: v for k, v in enumerate(programm)}
        )
        self._ic = 0  # Instruction Counter
        self._rbo = 0  # Relative Base Offset
        self.stdout = Queue()
        self.stdin = Queue()

    @classmethod
    def log(cls, *text):
        if cls.DEBUG:
            print(*text)

    @staticmethod
    def from_file(file):
        with open(file) as f:
            programm = [int(e) for e in f.read().split(',')]
        return Interpreter(programm)

    def put(self, value):
        """Adds value to stdin"""
        self.stdin.put(value)

    def stream(self):
        while not self.stdout.empty():
            yield self.stdout.get()

    def _read(self, amount, modes='') -> List[Ref]:
        modes = modes.zfill(amount)

        for mode in reversed(modes):
            cur = self._memory[self._ic]
            self._ic += 1

            if mode == '0':
                yield Ref(self, cur)
            elif mode == '1':
                yield Var(cur)
            elif mode == '2':
                yield Rel(self, cur)
            else:
                raise Exception('Unknown param mode')

    def __getitem__(self, key) -> Union[int, Tuple[int]]:
        """
        Returns value from memory. Can handle slices
        """

        if type(key) is slice:
            start = key.start
            stop = key.stop

            if start is None:
                start = min(self._memory.keys())
            if stop is None:
                stop = min(self._memory.keys())
            if key.step is None:
                step = 1

            return tuple(self._memory[i] for i in range(start, stop, step))

        return self._memory[key]

    def __setitem__(self, key, value: int):
        self._memory[key] = value

    def start(self):
        thread = Thread(target=self.run)
        thread.start()
        return thread

    def run(self):
        while True:
            op_code, *_ = self._read(1, modes='1')

            op = op_code() % 100
            modes = str(op_code())[:-2]

            if op == 1:  # Addition
                p1, p2, des = self._read(3, modes=modes)
                des(p1() + p2())

            elif op == 2:  # Multiply
                p1, p2, des = self._read(3, modes=modes)
                des(p1() * p2())

            elif op == 3:  # Set IC
                p1, *_ = self._read(1, modes=modes)
                p1(self.stdin.get())

            elif op == 4:  # PRINT
                p1, *_ = self._read(1, modes=modes)
                self.stdout.put(p1())

            elif op == 5:  # JUMP-IF-TRUE
                p1, p2, *_ = self._read(2, modes=modes)
                if p1() != 0:
                    self._ic = p2()

            elif op == 6:  # JUMP-IF-FALSE
                p1, p2, *_ = self._read(2, modes=modes)
                if p1() == 0:
                    self._ic = p2()

            elif op == 7:  # LESS-THEN
                p1, p2, p3, *_ = self._read(3, modes=modes)
                p3(bool(p1() < p2()))

            elif op == 8:  # EQUAL
                p1, p2, p3, *_ = self._read(3, modes=modes)
                p3(bool(p1() == p2()))

            elif op == 9:  # Set RBO
                p1, *_ = self._read(1, modes=modes)
                self._rbo = p1()

            elif op == 99:
                self.log('Stop program')
                break
            else:
                raise Exception(f'Unknown OP code {op}')

    def dump(self) -> Dict[int, int]:
        return self._memory.copy()
