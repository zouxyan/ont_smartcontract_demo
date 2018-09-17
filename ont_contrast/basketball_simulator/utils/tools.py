from ontology.ont_sdk import OntologySdk
from ontology.account.account import Address, Account
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.utils import util

import time
import json

# -------------------------------------------
# GLOBAL SETTINGS
# -------------------------------------------
rpc_addr = 'http://polaris3.ont.io:20336'
sdk = OntologySdk()
sdk.set_rpc(rpc_addr)
sdk.open_wallet('/Users/zou/PycharmProjects/ont_test/ont_contrast/demo/cli/wallet.json')

code = ''
addr = Address.address_from_vm_code(code)
contract_addr = addr.to_array()

abi = '{"functions":[{"name":"main","parameters":[{"name":"op","type":""},{"name":"args","type":""}],"returntype":""},{"name":"init","parameters":[{"name":"seed","type":""}],"returntype":""},{"name":"next_round","parameters":[{"name":"seed","type":""}],"returntype":""},{"name":"shoot","parameters":[{"name":"off_player","type":""},{"name":"def_player","type":""},{"name":"seconds","type":""},{"name":"team","type":""}],"returntype":""},{"name":"pass_ball","parameters":[{"name":"holder","type":""},{"name":"def_player","type":""},{"name":"team","type":""}],"returntype":""},{"name":"get_scores","parameters":[{"name":"","type":""}],"returntype":""},{"name":"get_curr_time","parameters":[{"name":"","type":""}],"returntype":""},{"name":"get_team_scores","parameters":[{"name":"","type":""}],"returntype":""},{"name":"pick_ball_holder","parameters":[{"name":"team","type":""},{"name":"is_first","type":""}],"returntype":""},{"name":"jump_ball","parameters":[{"name":"","type":""}],"returntype":""},{"name":"rand_player","parameters":[{"name":"team","type":""}],"returntype":""},{"name":"random_int_from_zero","parameters":[{"name":"num","type":""},{"name":"seed","type":""}],"returntype":""}]}'
abi = json.loads(abi)
abi_info = AbiInfo('0x' + addr.to_reverse_hex_str(), 'main', abi['functions'], [])

acc1 = sdk.get_wallet_manager().get_account('ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6', '1')


def get_from_hex(res):
    """
    hex to string
    :param res:
    :return:
    """
    return util.parse_neo_vm_contract_return_type_string(res)


def get_integer_from_hex(res):
    """
    hex to integer
    :param res:
    :return:
    """
    return util.parse_neo_vm_contract_return_type_integer(res)


def print_info(res):
    """
    print notify info
    :param res: json
    :return:
    """
    now = time.time()
    json_res = sdk.get_rpc().get_smart_contract_event_by_tx_hash(res)
    while json_res is None:
        json_res = sdk.get_rpc().get_smart_contract_event_by_tx_hash(res)
        time.sleep(0.1)
    print('checking tx cost %.2fs' % (time.time() - now))
    print(json_res)
    print('txid: %s' % res)
    # try:
    #     print('action:%s\nfrom_account:%s\nto_account:%s\namount:%s'
    #           % (get_from_hex(json_res['Notify'][0]['States'][0]),
    #              json_res['Notify'][0]['States'][1], json_res['Notify'][0]['States'][2],
    #              util.parse_neo_vm_contract_return_type_integer(json_res['Notify'][0]['States'][3])))
    # except Exception:
    #     print('wrong notify')


def get_states_list(txid, addr):
    """
    Put the events of addr in a list and return
    :param txid:
    :param addr:
    :return:
    """
    json_res = sdk.get_rpc().get_smart_contract_event_by_tx_hash(txid)
    while json_res is None:
        json_res = sdk.get_rpc().get_smart_contract_event_by_tx_hash(txid)
        time.sleep(0.1)
    notifies = json_res['Notify']
    states = []
    for i in range(len(notifies)):
        if notifies[i]['ContractAddress'] == addr:
            # print(notifies[i]['ContractAddress'])
            # print(get_from_hex(notifies[i]['States']))
            states.append(get_from_hex(notifies[i]['States']))
    return states