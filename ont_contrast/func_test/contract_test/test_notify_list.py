from boa.interop.System.Runtime import Notify


def main(op):
    if op == 'test':
        return notify_list()
    return False


def notify_list():
    Notify(['zou', 'xue', 'yan'])
    return True