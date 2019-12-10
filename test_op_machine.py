import pytest

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

    assert subject[:] == (1002, 4, 3, 4, 99)


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
    subject = Interpreter([109, 5, 109, -4, 204, 3, 99])

    subject.run()

    assert subject._rbo == 1
    assert subject.stdout.get() == 204


def test_read_from_somewhere():
    subject = Interpreter([4, 100, 99])

    subject.run()

    assert subject.stdout.get() == 0


@pytest.mark.parametrize('program,param,result', [
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, 1),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, 1),
])
def test_day_5_jump_test(program, param, result):
    subject = Interpreter(program)
    subject.put(param)
    subject.run()
    assert subject.get() == result


def test_day_9_quine_test(capsys):
    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    subject = Interpreter(program)

    subject.run()
    # subject.DEBUG = True
    # with capsys.disabled():
    #     print()
    #     print(f'  MEM| (IC: {subject._ic}, RBO: {subject._rbo})', subject[:])
    #     while not subject.finished:
    #         subject.step()
    #         print(f'  MEM| (IC: {subject._ic}, RBO: {subject._rbo})', subject[:])

    assert list(subject.stream()) == program


@pytest.mark.parametrize(
    'program,result',
    [
        ([1102, 34915192, 34915192, 7, 4, 7, 99, 0], 1219070632396864),
        ([104, 1125899906842624, 99], 1125899906842624),
    ]
)
def test_day_9_more_tests(program, result):
    subject = Interpreter(program)
    subject.run()
    assert subject.get() == result

