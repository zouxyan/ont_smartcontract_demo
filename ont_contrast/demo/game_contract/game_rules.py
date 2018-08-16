# conding=utf-8
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import Notify


def main(op, args):
    if op == 'join':
        return join(args[0], args[1])

    if op == 'start':
        pass

    if op == 'listen':
        return is_game_ready()

    if op == 'get_amounts':
        return get_amounts()

    if op == 'query':
        context = GetContext()
        value = Get(context, args[0])
        if value is None:
            return 'no'
        return value

    if op == 'delete':
        context = GetContext()
        value = Get(context, args[0])
        if value is None:
            return False
        Delete(context, args[0])
        return True


    return False


def join(addr, amount):
    # 临时这么搞
    info = {0: 'count', 1: 'acc1', 2: 'amount1', 3: 'acc2', 4: 'amount2', 5: 'acc3', 6: 'amount3'}
    context = GetContext()
    count = Get(context, 'count')
    if count is None:
        count = 0
    count += 1

    if count >= 3:
        Notify('No more seat')
        return False

    acc_key = info[2 * count - 1]
    amount_key = info[count * 2]

    Put(context, acc_key, addr)
    Put(context, amount_key, float(amount))
    Put(context, 'count', count)

    Notify('join successfully')
    return True


def is_game_ready():
    """
    for pre-exec
    :return:
    """
    context = GetContext()
    count = Get(context, 'count')
    amount1 = Get(context, 'amount1')
    amount2 = Get(context, 'amount2')
    amount3 = Get(context, 'amount3')

    def is_number(x):
        if x is None or type(x) is not float:
            return False
        return True

    if count == 3 and is_number(amount1) and is_number(amount2) and is_number(amount3):
        return True
    return False


def get_amounts():
    """
    after ready, gamer get the account balance, to check if the gamers has transfered their ont to
    contract
    :return: sum of amounts
    """
    if not is_game_ready():
        return 'Not Ready'

    context = GetContext()
    return Get(context, 'amount1') + Get(context, 'amount2') + Get(context, 'amount3')