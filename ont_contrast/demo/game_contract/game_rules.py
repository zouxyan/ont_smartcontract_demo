# conding=utf-8
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import Notify
import random


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

    Notify(acc_key)
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

    if ready, player get the account balance, to check if the players has transfered their ont to
    contract
    :return: sum of amounts
    """
    if not is_game_ready():
        return 'Not Ready'

    context = GetContext()
    return Get(context, 'amount1') + Get(context, 'amount2') + Get(context, 'amount3')


def roll_dice(player):
    """

    :param player: 玩家账户地址
    :return:
    """
    context = GetContext()
    if Get(context, 'acc1') != player and Get(context, 'acc2') != player and Get(context, 'acc3') != player:
        Notify('player not in the game')
        return False

    if Get(context, player) is not None:
        Notify('you dice twice')
        return False

    num = random.randint(1, 6)
    Put(context, player, num)
    Notify(num)
    # 最后一个玩家清算赌局
    if is_3_dices_on_table():
        acc1_num = Get(context, Get(context, 'acc1'))
        acc2_num = Get(context, Get(context, 'acc2'))
        acc3_num = Get(context, Get(context, 'acc3'))
        max_val = max(acc1_num, acc2_num, acc3_num)

        if acc1_num == max_val:
            Put(context, 'winner', Get(context, 'acc1'))
            pass  # 钱打给Get(context, 'acc1')

        elif acc2_num == max_val:
            Put(context, 'winner', Get(context, 'acc2'))
            pass
        else:
            Put(context, 'winner', Get(context, 'acc3'))
            pass
        Delete(context, 'count')  # 一旦count被删除，意味着下一场赌局的开始
    return True


def is_3_dices_on_table():
    """
    pre-exec
    :return:
    """
    context = GetContext()
    acc1_num = Get(context, Get(context, 'acc1'))
    acc2_num = Get(context, Get(context, 'acc2'))
    acc3_num = Get(context, Get(context, 'acc3'))

    if acc1_num is not None and acc2_num is not None and acc3_num is not None:
        return True
    return False


def get_res():
    context = GetContext()
    res = Get(context, 'winner')
    if res is None:
        return False
    return res