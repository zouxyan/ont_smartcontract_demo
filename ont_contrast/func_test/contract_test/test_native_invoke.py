from boa.interop.System.Storage import *
from boa.interop.System.Runtime import *
from boa.interop.System.ExecutionEngine import *
from boa.interop.Ontology.Native import Invoke

ctx = GetContext()
selfAddr = GetExecutingScriptHash()
contractAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')


def main(op, args):
    if op == 'to_sc':
        return to_sc(args[0])

    return False


def to_sc(acc):
    if not CheckWitness(acc):
        return False
    param = [acc, selfAddr, 10]
    res = Invoke(ver=1, contractAddress=contractAddress, method='transfer', param=[param])
    Notify(res)
    if res and res == b'\x01':
        Notify('transfer succeed')
        return True
    else:
        Notify('transfer failed')
        return False