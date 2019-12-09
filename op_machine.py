import sys


def read_input(_list: list):
    return {i: int(v) for i, v in enumerate(_list)}


class Interpreter:
    DEBUG = False

    def __init__(self, state) -> None:
        super().__init__()
        self.state = state
        self.ic = 0
        self._stdout = sys.stdout

    @classmethod
    def log(cls, *text):
        if cls.DEBUG:
            print(*text)

    def read(self, amount, modes=''):
        modes = modes.zfill(amount)

        for i in range(amount):
            cur = self.state[self.ic]
            self.ic += 1

            if modes[i] == '0':  # handle cur as address if mode 0
                yield self[cur]
            elif modes[i] == '0':  # handle cur as value if mode 1
                yield cur

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, key, value):
        self.state[key] = value

    def resolve(self, address, param_mode):
        if param_mode == 1:
            return address
        else:
            return self[address]

    def run(self):

        while True:
            op, *_ = self.read(1)
            param_modes = str(op)[:-2]

            if op == 1:  # Addition
                p1, p2, des = self.read(3)
                self[des] = p1 + p2

            elif op == 2:  # Multiply
                p1, p2, des = self.read(3)
                self[des] = self[p1] * self[p2]

            elif op == 3:  # Set
                p1, p2 = self.read(2)
                self[p1] = p2

            elif op == 4:  # PRINT
                p1, *_ = self.read(1)
                print(self[p1], end='', file=self._stdout)

            elif op == 99:
                self.log('Stop program')
                break
            else:
                raise Exception(f'Unknown OP code {op}')

        return [self.state[i] for i in range(len(self.state))]
