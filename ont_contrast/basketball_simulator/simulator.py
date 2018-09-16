from ontology.ont_sdk import OntologySdk
from ontology.account.account import Address, Account
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.utils import util
from ont_contrast.basketball_simulator.utils import tools

import time
import json
from random import randint, random

# -------------------------------------------
# GLOBAL SETTINGS
# -------------------------------------------
narrators = ["O'Neill", "VanGundy"]


class Simulator(object):
    def __init__(self, sdk, acc, code, abi_info, need_deploy):
        self.sdk = sdk
        self.acc = acc
        self.code = code
        self.addr = Address.address_from_vm_code(code)
        self.abi_info = abi_info
        self.contract_addr = self.addr.to_array()
        self.need_deploy = need_deploy

    def deploy_game(self):
        if not self.need_deploy:
            return False
        tx = self.sdk.neo_vm().make_deploy_transaction(self.code, True, 'all_star', 'v1.0', 'zou', '', '',
                                                       self.acc.get_address_base58(), 20000000000, 500)
        self.sdk.sign_transaction(tx, self.acc)
        return self.sdk.get_rpc().send_raw_transaction(tx)

    def init_game(self):
        func = self.abi_info.get_function('init')
        func.set_params_value((get_seed(),))
        res = self.sdk.neo_vm().send_transaction(self.contract_addr, self.acc, self.acc, 200000000, 500, func, False)
        return tools.get_states_list(res, self.addr.to_reverse_hex_str())

    def next_round(self, seed):
        func = self.abi_info.get_function('next_round')
        func.set_params_value((seed, ))
        res = self.sdk.neo_vm().send_transaction(self.contract_addr, self.acc, self.acc, 200000000, 500, func, False)
        return tools.get_states_list(res, self.addr.to_reverse_hex_str())

    def get_game_time(self):
        func = self.abi_info.get_function('get_curr_time')
        func.set_params_value((1,))
        time = tools.get_integer_from_hex(self.sdk.neo_vm().send_transaction(self.contract_addr, self.acc, self.acc,
                                                                             200000000, 500, func, True))
        minutes = int(time / 60)
        sec = time - 60 * minutes
        if minutes < 10:
            minutes = '0%d' % minutes
        else:
            minutes = str(minutes)
        if sec < 10:
            sec = '0%d' % sec
        else:
            sec = str(sec)
        return "***" + minutes + " : " + sec + "***"

    def get_team_scores(self):
        func = self.abi_info.get_function('get_team_scores')
        func.set_params_value((1,))
        scores = self.sdk.neo_vm().send_transaction(self.contract_addr, self.acc, self.acc, 200000000, 500, func, True)
        if scores[0] == '':
            ws = 0
        else:
            ws = tools.get_integer_from_hex(scores[0])
        if scores[1] == '':
            es = 0
        else:
            es = tools.get_integer_from_hex(scores[1])
        return '***' + str(ws) + ' : ' + str(es) + '***'

    def get_technical_statistics(self):
        func = self.abi_info.get_function('get_scores')
        func.set_params_value((1,))
        return self.sdk.neo_vm().send_transaction(self.contract_addr, self.acc, self.acc, 200000000, 500, func, True)


def get_narrator():
    return narrators[randint(0, 1)]


def show_technical_statistics(scores):
    west_s = scores[0]
    east_s = scores[1]
    func = lambda x: '0' if x is '' else str(tools.get_integer_from_hex(x))

    records = ['James: ' + func(west_s[0]), 'Durant: ' + func(west_s[1]), 'Davis: ' + func(west_s[2]),
               'Curry: ' + func(west_s[3]), 'Harden: ' + func(west_s[4]), 'Leonard: ' + func(east_s[0]),
               'Antetokounmpo: ' + func(east_s[1]), 'Embiid: ' + func(east_s[2]), 'Wall: ' + func(east_s[3]),
               'Oladipo: ' + func(east_s[4])]

    return records


def get_seed():
    return int(random() * 10000000000)


if __name__ == '__main__':
    game = Simulator(tools.sdk, tools.acc1, tools.code, tools.abi_info, True)
    print(game.deploy_game())
    time.sleep(2)

    print('比赛开始！！！本场比赛由%s和%s为您解说' % (narrators[0], narrators[1]))
    init_event = game.init_game()
    print(get_narrator() + ': ' + init_event[0] + ' 比赛时间：' + game.get_game_time())
    print('\n\n')

    is_end = False
    while not is_end:
        events = game.next_round(get_seed())
        for i in events:
            if i == 'end':
                is_end = True
                break
            print(get_narrator() + ': ' + i)
            time.sleep(1)
        print(get_narrator() + ': 当前比分: ' + game.get_team_scores())
        print(get_narrator() + ': 比赛时间: ' + game.get_game_time())
        print('\n')

    print(get_narrator() + ": 比赛结束，下面最终比分，以及技术统计")
    print('西部 TO 东部' + game.get_team_scores())
    scores = show_technical_statistics(game.get_technical_statistics())
    for i in scores:
        print(i)
