from boa.interop.System.Storage import *
from boa.interop.System.Runtime import *
from boa.interop.System.ExecutionEngine import *
from boa.interop.Ontology.Native import Invoke


ctx = GetContext()
self_addr = GetExecutingScriptHash()


def main(op, addr):
    if op == 'check':
        return check(addr)

    return False


def check(addr):
    return addr == self_addr

