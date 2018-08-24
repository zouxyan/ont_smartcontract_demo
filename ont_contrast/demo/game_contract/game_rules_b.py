"""
根据更新的API，重写合约
"""
from boa.interop.System.Storage import *
from boa.interop.System.Runtime import *
from boa.interop.System.ExecutionEngine import *
from boa.builtins import list as sc_list, range as sc_range, concat
from boa.interop.Ontology.Native import Invoke

import random

CTX = GetContext()
SELF_ADDR = GetExecutingScriptHash()
CONTRACT_ADDR = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')


def main(op, args):
    if op == 'join':
        return join(args[0], args[1])

    return False


def join(acc, amount):
    """
    玩家入局，执行游戏逻辑
    :param acc: 用户账户，具体输入格式不明，toScriptHash??
    :param amount: 金额
    :return: 完成返回True，结束
    """
    players_in_game = Get(CTX, 'players_in_game')
    if players_in_game is None:
        players_in_game = 0
    round_num = players_in_game / 3
    id_in_round = players_in_game % 3
    dice = random.randint(1, 6)

    param = [acc, SELF_ADDR, amount]
    res = Invoke(ver=1, contractAddress=CONTRACT_ADDR, method='transfer', param=[param])
    if not res or res != b'\x01':
        Notify('bet tranfer failed')
        return False

    player_id = concat(concat(str(round_num), '_'), str(id_in_round))
    Put(CTX, player_id, sc_list([acc, dice, amount]))
    Put(CTX, 'players_in_game', players_in_game + 1) # 并发问题？？？应该没有

    res_info = ''
    if id_in_round == 2:
        acc_list = [Get(CTX, concat(concat(str(round_num), '_'), str(i))) for i in sc_range(0, 3)]
        max_dice = 0
        max_acc = acc_list[0][0]
        for i in sc_range(0, 3):
            if acc_list[i][1] > max_dice:
                max_dice = acc_list[i][1]
                max_acc = acc_list[i][0]
        bonus = sum([acc_list[i][2] for i in sc_range(0, 3)])
        param = [SELF_ADDR, max_acc, bonus]
        res = Invoke(ver=1, contractAddress=CONTRACT_ADDR, method='transfer', param=[param])
        if not res or res != b'\x01':
            Notify('settle transfer failed')
            return False
        res_info = concat(concat(max_acc, ' win '), str(bonus))
    Notify(concat(concat(concat('your dice is ', str(dice)), concat(' your id is ', player_id)), res_info))
    return True
