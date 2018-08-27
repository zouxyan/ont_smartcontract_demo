from boa.interop.System.Runtime import *


def Main(op, args):
    Notify(0)
    if op == 'check':
        Notify(1)
        return check(args[0])
    return False


def check(acc):
    if CheckWitness(acc):
        Notify(2)
    Notify(3)
    return False