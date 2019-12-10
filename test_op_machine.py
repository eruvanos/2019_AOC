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

    assert subject[:5] == (1002, 4, 3, 4, 99)


def test_set():
    subject = Interpreter([3, 0, 99])
    subject.put(5)

    subject.run()

    assert subject[0] == 5


def test_out():
    subject = Interpreter([4, 0, 99])

    subject.run()

    assert subject.stdout.get() == 4


def test_relative_mode():
    subject = Interpreter([109, 5, 204, -1, 99])

    subject.run()

    assert subject._rbo == 5
    assert subject.stdout.get() == 99

def test_read_from_somewhere():
    subject = Interpreter([4, 100, 99])

    subject.run()

    assert subject.stdout.get() == 0
