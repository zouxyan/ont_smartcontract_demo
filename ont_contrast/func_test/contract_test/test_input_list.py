from boa.interop.System.Runtime import *


def Main(op, args):
    if op == 'test':
        Notify(0)
        return test(args[0])


def test(arr):
    Notify(1)
    for x in arr:
        Notify(x[2])
        Notify(x)
    return True