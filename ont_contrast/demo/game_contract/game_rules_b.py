"""
根据更新的API，重写合约
"""
from boa.interop.System.Storage import *
from boa.interop.System.Runtime import *
from boa.interop.System.ExecutionEngine import *
from boa.builtins import list as sc_list, range as sc_range, concat
from boa.interop.Ontology.Native import Invoke

import random

ctx = GetContext()
self_addr = GetExecutingScriptHash()
contract_address = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')


def main(op, args):
    pass


def join(acc, amount):
    players_in_game = Get(ctx, 'players_in_game')
    if players_in_game is None:
        players_in_game = 0
    round_num = players_in_game / 3
    id_in_round = players_in_game % 3
    dice = random.randint(1, 6)

    param = [acc, self_addr, amount]
    res = Invoke(ver=1, contractAddress=contract_address, method='transfer', param=[param])
    if not res or res != b'\x01':
        Notify('bet tranfer failed')
        return False

    player_id = concat(concat(str(round_num), '_'), str(id_in_round))
    Put(ctx, player_id, sc_list([acc, dice, amount]))
    Put(ctx, 'players_in_game', players_in_game + 1) # 并发问题？？？应该没有
    Notify(concat(concat('your dice is ', str(dice)), concat('your id is ', player_id)))

    if id_in_round == 2:
        acc_list = [Get(ctx, concat(concat(str(round_num), '_'), str(i))) for i in sc_range(0, 3)]
        max_dice = 0
        max_acc = acc_list[0][0]
        for i in sc_range(0, 3):
            if acc_list[i][1] > max_dice:
                max_dice = acc_list[i][1]
                max_acc = acc_list[i][0]
        param = [self_addr, max_acc, sum([acc_list[i][2] for i in sc_range(0, 3)])]
        res = Invoke(ver=1, contractAddress=contract_address, method='transfer', param=[param])
        if not res or res != b'\x01':
            Notify('settle tranfer failed')
            return False
    return True
