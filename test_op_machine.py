from io import StringIO

from op_machine import Interpreter


def test_add():
    subject = Interpreter([1, 0, 0, 0, 99])

    subject.run()

    assert subject[0] == 2


def test_multiply():
    subject = Interpreter([2, 3, 0, 3, 99])

    subject.run()

    assert subject[3] == 6


def test_set():
    subject = Interpreter([3, 0, 10, 99])

    subject.run()

    assert subject[0] == 10


def test_print():
    subject = Interpreter([4, 0, 99])
    subject._stdout = StringIO()

    subject.run()

    assert subject._stdout.getvalue() == '4'
