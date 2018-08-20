from boa.interop.System.Storage import *
from boa.interop.System.Runtime import *
from boa.interop.System.ExecutionEngine import *
from boa.interop.Ontology.Native import Invoke

ctx = GetContext()
selfAddr = GetExecutingScriptHash()
contractAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
acc = b'\x47\x56\xc9\xdd\x82\x9b\x21\x42\x88\x3a\xdb\xe1\xae\x4f\x86\x89\xa1\xf6\x73\xe9' # ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6


def main(op):
    if op == 'to_sc':
        return to_sc(acc)

    if op == 'to_acc':
        return to_acc(acc)

    return False


def to_sc(acc):
    param = [acc, selfAddr, 10]
    res = Invoke(ver=1, contractAddress=contractAddress, method='transfer', param=[param])
    Notify(res)
    if res and res == b'\x01':
        Notify('transfer succeed')
        return True
    else:
        Notify('transfer failed')
        return False


def to_acc(acc):
    param = [selfAddr, acc, 10]
    res = Invoke(ver=1, contractAddress=contractAddress, method='transfer', param=[param])
    Notify(res)
    if res and res == b'\x01':
        Notify('transfer succeed')
        return True
    else:
        Notify('transfer failed')
        return False