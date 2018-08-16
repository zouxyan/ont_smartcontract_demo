from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import Notify, Log, GetTime


def Main(operation, domain, owner):
    if operation == 'Query':
        Notify(1)
        return Query(domain)

    if operation == 'Register':
        Notify(2)
        return Register(domain, owner + GetTime())

    if operation == 'Delete':
        Notify(3)
        return Delete1(domain)
    return False

def Query(domain):
    context = GetContext()
    owner = Get(context, domain)
    if owner == None:
        return False
    return owner

def Register(domain, owner):
    context = GetContext()
    occupy = Get(context, domain)
    if occupy != None:
        return False
    Put(context, domain, owner)
    return True

def Delete1(domain):
    context = GetContext()
    if Get(context, domain) == None:
        return False
    Delete(context, domain)
    return True
