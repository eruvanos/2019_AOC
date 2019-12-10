from op_machine import Interpreter


def test_add():
    subject = Interpreter([1, 0, 0, 0, 99])

    subject.run()

    assert subject[0] == 2


def test_multiply():
    subject = Interpreter([2, 3, 0, 3, 99])

    subject.run()

    assert subject[3] == 6


def test_multiply_param_modes():
    subject = Interpreter([1002, 4, 3, 4, 33])

    subject.run()

    assert subject.dump() == (1002, 4, 3, 4, 99)


def test_set():
    subject = Interpreter([3, 0, 99])
    subject.stdin.insert(0, 5)

    subject.run()

    assert subject[0] == 5


def test_print():
    subject = Interpreter([4, 0, 99])

    subject.run()

    assert subject.stdout == [4]
