from boa.interop.System.Runtime import *
from boa.interop.System.Storage import *
from boa.interop.System.ExecutionEngine import *
from boa.interop.Ontology.Native import Invoke
from boa.interop.System.Block import GetTimestamp
from boa.interop.System.Blockchain import GetHeader, GetHeight
from boa.builtins import *

arr = ['a', 'b', 'c']


def main(op, args):
    if op == 'test':
        test(args)

    if op == 'test1':
        return test1()

    return False


def test(args):
    time = GetTime()
    Notify(0.3 * 10)

    res = int(sha1(time))
    aa = res / 3
    res -= 3 * aa

    if res is 0:
        Notify(arr[res])
        return
    if res is 1:
        Notify(arr[res])
        return
    if res == 2:
        Notify(arr[2])
        return

    Notify(res)
    Notify(100 % 3)


def test1():
    return [arr, arr]