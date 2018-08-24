def Main(op, args):
    if op == 'test':
        return test()
    return False


def test():
    return 'result'