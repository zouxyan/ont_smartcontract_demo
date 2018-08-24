from boa.interop.System.Runtime import *
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash

SELF_ADDR = GetExecutingScriptHash()


def main(op, args):
    if op == 'check':
        return check(SELF_ADDR)
    return False


def check(acc):
    Notify(acc)
    return str(acc)