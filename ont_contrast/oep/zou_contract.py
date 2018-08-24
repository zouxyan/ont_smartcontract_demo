"""
OEP4协议python实现实例
用来在ONT上发布代币

已经跑通
"""

from boa.interop.System.Storage import *
from boa.interop.System.Runtime import CheckWitness, Notify
from boa.builtins import concat

# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------

ctx = GetContext()

NAME = 'xue'
SYMBOL = 'XUE'
OWNER = bytearray(b'GV\xc9\xdd\x82\x9b!B\x88:\xdb\xe1\xaeO\x86\x89\xa1\xf6s\xe9')
DECIMALS = 8
FACTOR = 1000
TOTAL_AMOUNT = 1000

TRANSFER_PREFIX = bytearray(b'\x01')
APPROVE_PREFIX = bytearray(b'\x02 ')
TOLAL_KEY = 'total_supply'


def Main(op, args):
    """
    合约入口，需注意op的值必须和函数名相同，方便SDK调用

    :param op: 调用的函数
    :param args: 函数参数，数组形式
    :return:
    """
    if op == 'init':
        return init()

    if op == 'total_supply':
        return total_supply()

    if op == 'name':
        return name()

    if op == 'symbol':
        return symbol()

    if op == 'transfer':
        if len(args) != 3:
            return False
        from_acc = args[0]
        to_acc = args[1]
        value = args[2]
        return transfer(from_acc, to_acc, value)

    if op == 'transfer_multi':
        return transfer_multi(args[0])

    if op == 'approve':
        if len(args) != 3:
            return False
        owner = args[0]
        spender = args[1]
        if len(owner) != 20 or len(spender) != 20:
            return False
        value = args[2]
        return approve(owner, spender, value)

    if op == 'transfer_from':
        if len(args) != 4:
            return False
        spender = args[0]
        from_acc = args[1]
        to_acc = args[2]
        if len(spender) != 20 or len(from_acc) != 20 or len(to_acc) != 20:
            return False
        value = args[3]
        return transfer_from(spender, from_acc, to_acc, value)

    if op == 'balance_of':
        if len(args) != 1:
            return False
        return balance_of(args[0])

    if op == 'allowance':
        if len(args) != 2:
            return False
        return allowance(args[0], args[1])

    if op == 'decimal':
        return decimal()

    return False


def init():
    """
    代币初始化函数
    :return:
    """
    if Get(ctx, TOLAL_KEY) is not None:
        return False

    total = TOTAL_AMOUNT * FACTOR
    Put(ctx, TOLAL_KEY, total)
    Put(ctx, concat(TRANSFER_PREFIX, OWNER), total)
    Notify(['transfer', '', OWNER, total])
    return True


def transfer(acc_from, acc_to, value):
    """
    转账
    :param acc_from: 长度必为20，输入为bytearray
    :param acc_to: 同上
    :param value: 非负整数，1 = 1e-8 ZOU
    :return:
    """
    if acc_from == acc_to or value == 0:
        return True
    if value < 0 or not CheckWitness(acc_from) or len(acc_to) != 20:
        return False
    from_key = concat(TRANSFER_PREFIX, acc_from)
    from_amount = Get(ctx, from_key)
    if from_amount is None or from_amount < value:
        return False
    if from_amount == value:
        Delete(ctx, from_key)
    else:
        Put(ctx, from_key, from_amount - value)

    to_key = concat(TRANSFER_PREFIX, acc_to)
    to_amount = Get(ctx, to_key)
    Put(ctx, to_key, to_amount + value)
    Notify(['transfer', acc_from, acc_to, value])
    return True


def transfer_multi(arr):
    """
    多组转账，一笔交易
    :param arr: list，每个元素为一笔转账
    :return:
    """
    for p in arr:
        if len(p) != 3:
            return False
        if not transfer(p[0], p[1], p[2]):
            return False
    return True


def balance_of(addr):
    """
    查询账户余额
    :param addr:
    :return:
    """
    return Get(ctx, concat(TRANSFER_PREFIX, addr))


def approve(owner, spender, amount):
    """
    资产使用权
    :param owner:
    :param spender:
    :param amount:
    :return:
    """
    if amount < 0 or not CheckWitness(owner) or Get(ctx, concat(TRANSFER_PREFIX, owner)) < amount:
        return False
    key = concat(concat(APPROVE_PREFIX, owner), spender)
    allow = Get(ctx, key)
    if allow is None:
        Put(ctx, key, amount)
    else:
        Put(ctx, key, allow + amount)

    Notify(['approve', owner, spender, amount])
    return True


def transfer_from(spender, from_acc, to_acc, amount):
    """
    获得他人资产使用权后，使用他人资产向其他账户转账
    :param spender:
    :param from_acc:
    :param to_acc:
    :param amount:
    :return:
    """
    if amount < 0 or not CheckWitness(spender):
        return False
    approve_key = concat(concat(APPROVE_PREFIX, OWNER), spender)
    approve_value = Get(ctx, approve_key)
    if approve_value is None or approve_value < amount:
        return False
    if approve_value == amount:
        Delete(ctx, approve_key)
    else:
        Put(ctx, approve_key, approve_value - amount)

    if len(from_acc) != 20 or len(to_acc) != 20:
        return False
    from_key = concat(TRANSFER_PREFIX, from_acc)
    from_balance = Get(ctx, from_key)
    if from_balance is None or from_balance < amount:
        return False
    if from_balance == amount:
        Delete(ctx, from_key)
    else:
        Put(ctx, from_key, from_balance - amount)

    to_key = concat(TRANSFER_PREFIX, to_acc)
    to_balance = Get(ctx, to_key)
    Put(ctx, to_key, to_balance + amount)
    Notify(['transfer', from_acc, to_acc, amount])
    return True


def allowance(owner, spender):
    """
    查询owner能使用spender的资产数目
    :param owner:
    :param spender:
    :return:
    """
    return Get(ctx, concat(concat(APPROVE_PREFIX, owner), spender))


def decimal():
    """
    ZOU精度，1单位=1e-DECIMALS ZOU
    :return:
    """
    return DECIMALS


def symbol():
    """
    代币符号ZOU
    :return:
    """
    return SYMBOL


def total_supply():
    """
    总共多少单位ZOU
    :return:
    """
    return TOTAL_AMOUNT * FACTOR


def name():
    """
    名字
    :return:
    """
    return NAME
