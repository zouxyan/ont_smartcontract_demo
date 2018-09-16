from boa.interop.System.Runtime import *
from boa.interop.System.Storage import *
from boa.interop.System.ExecutionEngine import *
from boa.interop.Ontology.Native import Invoke
from boa.builtins import *
from boa.interop.Neo.App import RegisterAppCall


def main(op, args):
    if op == 'invoke_a':
        invoke_a(args[0])

    if op == 'invoke_a1':
        return invoke_a1(args[0])

    return False


def invoke_a(addr):
    sc_a = RegisterAppCall(addr, 'op', 'args')
    res = sc_a('test', 'sth')
    Notify(res)


def invoke_a1(addr):
    sc_a = RegisterAppCall(addr, 'op', 'args')
    res = sc_a('test1', '')
    return res
