from boa.interop.System.Runtime import *
from boa.interop.Ontology.Native import *
from boa.interop.System.ExecutionEngine import *
from boa.builtins import state

contractAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
selfAddr1 = GetExecutingScriptHash()


def Main(operation, args):
    if operation == 'to_sc':
        from_acct = args[0]
        amount = args[1]
        return to_sc(from_acct, amount)

    if operation == 'from_sc':
        to_acc = args[0]
        amount = args[1]
        return from_sc(to_acc, amount)
    return False


def to_sc(from_acct, amount):
    if CheckWitness(from_acct):
        param = makeState(from_acct, selfAddr1, amount)
        res = Invoke(1, contractAddress, 'transfer', [param])
        Notify(res)
        if res and res == b'\x01':
            Notify("succeed")
        else:
            Notify("failed")


def from_sc(to_acc, amount):
    param = makeState(selfAddr1, to_acc, amount)
    res = Invoke(1, contractAddress, 'transfer', [param])
    Notify(res)
    if res and res == b'\x01':
        Notify("succeed")
    else:
        Notify("failed")


def makeState(fromacct,toacct,amount):
    return state(fromacct, toacct, amount)