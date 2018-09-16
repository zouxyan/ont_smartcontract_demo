from ontology.utils import util
from unittest import TestCase
from ont_contrast.basketball_simulator.utils import tools
import time

# -------------------------------------------
# GLOBAL SETTINGS
# -------------------------------------------
seed = int(time.time() * 100000)
sdk = tools.sdk
code = tools.code
acc1 = tools.acc1
abi_info = tools.abi_info
contract_addr = tools.contract_addr
addr = tools.addr


class TestGame(TestCase):
    """
    unit test cases for contract game
    """

    def test_deploy_contract(self):
        tx = sdk.neo_vm().make_deploy_transaction(code, True, 'all_star', 'v1.0', 'zou', '', '',
                                             acc1.get_address_base58(), 20000000000, 500)
        sdk.sign_transaction(tx, acc1)
        res = sdk.get_rpc().send_raw_transaction(tx)
        print(res)

    def test_random_num(self):
        func = abi_info.get_function('random_int_from_zero')
        func.set_params_value((10, seed))
        # for i in range(100):
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000000, 500, func, True)
        print(util.parse_neo_vm_contract_return_type_integer(res))
            # time.sleep(1)

    def test_init(self):
        func = abi_info.get_function('init')
        func.set_params_value((seed, ))
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000000, 500, func, False)
        print(tools.get_states_list(res, addr.to_reverse_hex_str()))

    def test_get_scores(self):
        func = abi_info.get_function('get_scores')
        func.set_params_value((1, ))
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000000, 500, func, True)
        print(res)

    def test_get_team_scores(self):
        func = abi_info.get_function('get_team_scores')
        func.set_params_value((1, ))
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000000, 500, func, True)
        print(res)

    def test_next_round(self):
        func = abi_info.get_function('next_round')
        func.set_params_value((seed, ))
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000000, 500, func, False)
        print(tools.get_states_list(res, addr.to_reverse_hex_str()))
        # tools.print_info(res)
        # print(addr.to_reverse_hex_str())

    def test_jump_ball(self):
        func = abi_info.get_function('jump_ball')
        func.set_params_value((seed,))
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000000, 500, func, False)
        tools.print_info(res)

    def test_get_curr_time(self):
        func = abi_info.get_function('get_curr_time')
        func.set_params_value((1, ))
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000000, 500, func, True)
        print(res)
