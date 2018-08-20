"""
OEP4协议python实现
用来在ONT上发布代币
尚且有多点不明：  1 BigInteger具体使用是否正确
                2 ont团队的neo-boa尚未放出，测试无法进行
                3 transfer与approve事件机制尚无解决方案
                日期：2018, 8, 20
"""

from boa.interop.System.Storage import *
from boa.interop.System.Runtime import CheckWitness
from boa.interop.BigInteger import BigInteger
from boa.builtins import concat, range

# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------

ctx = GetContext()

NAME = 'zou'
SYMBOL = 'ZOU'
OWNER = 'ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6' # script_hash ??
DECIMALS = 8
FACTOR = 100000000
TOTAL_AMOUNT = 100000000 * FACTOR

TRANSFER_PREFIX = '01'
APPROVE_PREFIX = '02'


def main(op, args):
    if op == 'init':
        return init()

    if op == 'total_supply':
        return TOTAL_AMOUNT

    if op == 'name':
        return NAME

    if op == 'symbol':
        return SYMBOL

    if op == 'transfer':
        if len(args) != 3:
            return False
        from_acc = args[0]
        to_acc = args[1]
        value = BigInteger(args[2])
        return transfer(from_acc, to_acc, value)

    if op == 'transfer_multi':
        return transfer_multi(args)

    if op == 'approve':
        if len(args) != 3:
            return False
        owner = args[0]
        spender = args[1]
        if len(owner) != 20 or len(spender) != 20:
            return False
        value = BigInteger(args[2])
        return approve(owner, spender, value)

    if op == 'transfer_from':
        if len(args) != 4:
            return False
        spender = args[0]
        from_acc = args[1]
        to_acc = args[2]
        if len(spender) != 20 or len(from_acc) != 20 or len(to_acc) != 20:
            return False
        value = BigInteger(args[2])
        return transfer_from(spender, from_acc, to_acc, value)

    if op == 'balance_of':
        if len(args) != 1:
            return False
        return balance_of(args[0])

    if op == 'allowence':
        if len(args) != 2:
            return False
        return allowence(args[0], args[1])

    if op == 'decimals':
        return DECIMALS

    return False


def init():
    total_supply = Get(ctx, 'total_supply')
    if total_supply is not None:
        return False

    Put(ctx, concat(TRANSFER_PREFIX, OWNER), TOTAL_AMOUNT)
    Put(ctx, 'total_supply', TOTAL_AMOUNT)
    return True


def transfer(acc_from, acc_to, value: BigInteger): # ?? BigInteger???
    if value < 0 or not CheckWitness(acc_from) or len(acc_to) != 20:
        return False
    from_key = concat(TRANSFER_PREFIX, acc_from)
    from_amount = Get(ctx, from_key)
    if from_amount < value:
        return False
    if from_amount == value:
        Delete(ctx, from_key)
    else:
        Put(ctx, from_key, from_amount - value)

    to_key = concat(TRANSFER_PREFIX, acc_to)
    to_amount = Get(ctx, to_key)
    Put(ctx, to_key, to_amount + value)
    # event???
    return True


def transfer_multi(arr):
    for i in range(0, len(arr)):
        # ?? 如何设计每笔交易的state
        state = arr[i].split(':')
        if not transfer(state[0], state[1], BigInteger(state[2])):
            raise Exception()
    return True


def balance_of(addr):
    return BigInteger(Get(ctx, concat(TRANSFER_PREFIX, addr)))


def total_supply():
    return BigInteger(Get(ctx, 'total_supply'))


def approve(owner, spender, amount: BigInteger):
    if amount < 0 or not CheckWitness(owner) or BigInteger(Get(ctx, concat(TRANSFER_PREFIX, owner))) < amount:
        return False
    Put(ctx, concat(concat(APPROVE_PREFIX, owner), spender), amount)
    return True


def transfer_from(spender, from_acc, to_acc, amount: BigInteger):
    if amount < 0 or not CheckWitness(spender):
        return False
    approve_key = concat(concat(APPROVE_PREFIX, OWNER), spender)
    approve_value = BigInteger(Get(ctx, approve_key))
    if approve_value < amount:
        return False
    if approve_value == amount:
         Delete(ctx, approve_key)
    else:
        Put(ctx, approve_key, approve_value - amount)

    return transfer(from_acc, to_acc, amount)


def allowence(owner, spender):
    return Get(ctx, concat(concat(APPROVE_PREFIX, owner), spender))