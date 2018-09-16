from ontology.ont_sdk import OntologySdk
from ontology.account.account import Address, Account
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.utils import util
from unittest import TestCase
from collections import namedtuple

import time
import json

# -------------------------------------------
# GLOBAL SETTINGS
# -------------------------------------------
rpc_addr = 'http://polaris3.ont.io:20336'
sdk = OntologySdk()
sdk.set_rpc(rpc_addr)
sdk.open_wallet('/Users/zou/PycharmProjects/ont_test/ont_contrast/demo/cli/wallet.json')

code = '0133c56b6a00527ac46a51527ac46a00c304696e69749c64090065fb086c7566616a00c30c746f74616c5f737570706c799c6409006525026c7566616a00c3046e616d659c6409006500026c7566616a00c30673796d626f6c9c640900651e026c7566616a00c3087472616e736665729c6440006a51c3c0539e640700006c7566616a51c300c36a52527ac46a51c351c36a53527ac46a51c352c36a54527ac46a52c36a53c36a54c3527265c0066c7566616a00c30e7472616e736665725f6d756c74699c640e006a51c300c36533066c7566616a00c307617070726f76659c645a006a51c3c0539e640700006c7566616a51c300c36a55527ac46a51c351c36a56527ac46a55c3c001149e630d006a56c3c001149e64080061006c7566616a51c352c36a54527ac46a55c36a56c36a54c352726529046c7566616a00c30d7472616e736665725f66726f6d9c6483006a51c3c0549e640700006c7566616a51c300c36a56527ac46a51c351c36a52527ac46a51c352c36a53527ac46a56c3c001149e6317006a52c3c001149e630d006a53c3c001149e64080061006c7566616a51c353c36a54527ac46a56c36a52c36a53c36a54c35379517955727551727552795279547275527275652f016c7566616a00c30a62616c616e63655f6f669c641c006a51c3c0519e640700006c7566616a51c300c365b7046c7566616a00c309616c6c6f77616e63659c6422006a51c3c0529e640700006c7566616a51c300c36a51c351c37c6575006c7566616a00c307646563696d616c9c6409006550006c756661006c756654c56b036368656a00527ac46a00c36c756655c56b0400e1f5056a00527ac40400e1f5056a51527ac46a51c36a00c3956c756654c56b036368656a00527ac46a00c36c756654c56b586a00527ac46a00c36c756657c56b6a00527ac46a51527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a52527ac40202206a53527ac46a52c36a53c36a00c37e6a51c37e7c681253797374656d2e53746f726167652e476574616c75660121c56b6a00527ac46a51527ac46a52527ac46a53527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a54527ac4144756c9dd829b2142883adbe1ae4f8689a1f673e96a55527ac401016a56527ac40202206a57527ac46a53c3009f6328006a00c3681b53797374656d2e52756e74696d652e436865636b5769746e657373619164080061006c7566616a57c36a55c37e6a00c37e6a58527ac46a54c36a58c37c681253797374656d2e53746f726167652e476574616a59527ac46a59c30087630d006a59c36a53c39f64080061006c7566616a59c36a53c39c6425006a54c36a58c37c681553797374656d2e53746f726167652e44656c65746561622800616a54c36a58c36a59c36a53c3945272681253797374656d2e53746f726167652e50757461616a51c3c001149e630d006a52c3c001149e64080061006c7566616a56c36a51c37e6a5a527ac46a54c36a5ac37c681253797374656d2e53746f726167652e476574616a5b527ac46a5bc30087630d006a5bc36a53c39f64080061006c7566616a5bc36a53c39c6425006a54c36a5ac37c681553797374656d2e53746f726167652e44656c65746561622800616a54c36a5ac36a5bc36a53c3945272681253797374656d2e53746f726167652e50757461616a56c36a52c37e6a5c527ac46a54c36a5cc37c681253797374656d2e53746f726167652e476574616a5d527ac46a54c36a5cc36a5dc36a53c3935272681253797374656d2e53746f726167652e50757461087472616e736665726a51c36a52c36a53c354c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c75660111c56b6a00527ac46a51527ac46a52527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a53527ac401016a54527ac40202206a55527ac46a52c3009f634f006a00c3681b53797374656d2e52756e74696d652e436865636b5769746e6573736191632a006a53c36a54c36a00c37e7c681253797374656d2e53746f726167652e476574616a52c39f64080061006c7566616a55c36a00c37e6a51c37e6a56527ac46a53c36a56c37c681253797374656d2e53746f726167652e476574616a57527ac46a57c300876426006a53c36a56c36a52c35272681253797374656d2e53746f726167652e50757461622800616a53c36a56c36a57c36a52c3935272681253797374656d2e53746f726167652e507574616107617070726f76656a00c36a51c36a52c354c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c756656c56b6a00527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a51527ac401016a52527ac46a51c36a52c36a00c37e7c681253797374656d2e53746f726167652e476574616c756659c56b6a00527ac4006a52527ac46a00c3c06a53527ac4616a52c36a53c39f6445006a00c36a52c3c36a51527ac46a52c351936a52527ac46a51c3c0539e640700006c7566616a51c300c36a51c351c36a51c352c3527265140063bdff006c756662b6ff616161516c75660117c56b6a00527ac46a51527ac46a52527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a53527ac401016a54527ac46a00c36a51c39c630b006a52c3009c64080061516c7566616a52c3009f6332006a00c3681b53797374656d2e52756e74696d652e436865636b5769746e6573736191630d006a51c3c001149e64080061006c7566616a54c36a00c37e6a55527ac46a53c36a55c37c681253797374656d2e53746f726167652e476574616a56527ac46a56c30087630d006a56c36a52c39f64080061006c7566616a56c36a52c39c6425006a53c36a55c37c681553797374656d2e53746f726167652e44656c65746561622800616a53c36a55c36a56c36a52c3945272681253797374656d2e53746f726167652e50757461616a54c36a51c37e6a57527ac46a53c36a57c37c681253797374656d2e53746f726167652e476574616a58527ac46a53c36a57c36a58c36a52c3935272681253797374656d2e53746f726167652e50757461087472616e736665726a00c36a51c36a52c354c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c75665fc56b681953797374656d2e53746f726167652e476574436f6e74657874616a00527ac4144756c9dd829b2142883adbe1ae4f8689a1f673e96a51527ac40400e1f5056a52527ac40400e1f5056a53527ac401016a54527ac40c746f74616c5f737570706c796a55527ac46a00c36a55c37c681253797374656d2e53746f726167652e47657461009e640700006c7566616a53c36a52c3956a56527ac46a00c36a55c36a56c35272681253797374656d2e53746f726167652e507574616a00c36a54c36a51c37e6a56c35272681253797374656d2e53746f726167652e50757461087472616e73666572006a51c36a56c354c176c9681553797374656d2e52756e74696d652e4e6f7469667961516c75665ec56b6a00527ac46a51527ac46a51c36a00c3946a52527ac46a52c3c56a53527ac4006a54527ac46a00c36a55527ac461616a00c36a51c39f6433006a54c36a55c3936a56527ac46a56c36a53c36a54c37bc46a54c351936a54527ac46a55c36a54c3936a00527ac462c8ff6161616a53c36c7566'
addr = Address.address_from_vm_code(code)
contract_addr = addr.to_byte_array()

abi = '{"functions":[{"name":"Main","parameters":[{"name":"op","type":""},{"name":"args","type":""}],"returntype":""},{"name":"init","parameters":[{"name":"","type":""}],"returntype":""},{"name":"transfer","parameters":[{"name":"acc_from","type":""},{"name":"acc_to","type":""},{"name":"value","type":""}],"returntype":""},{"name":"transfer_multi","parameters":[{"name":"arr","type":""}],"returntype":""},{"name":"balance_of","parameters":[{"name":"addr","type":""}],"returntype":""},{"name":"approve","parameters":[{"name":"owner","type":""},{"name":"spender","type":""},{"name":"amount","type":""}],"returntype":""},{"name":"transfer_from","parameters":[{"name":"spender","type":""},{"name":"from_acc","type":""},{"name":"to_acc","type":""},{"name":"amount","type":""}],"returntype":""},{"name":"allowance","parameters":[{"name":"owner","type":""},{"name":"spender","type":""}],"returntype":""},{"name":"decimal","parameters":[{"name":"","type":""}],"returntype":""},{"name":"symbol","parameters":[{"name":"","type":""}],"returntype":""},{"name":"total_supply","parameters":[{"name":"","type":""}],"returntype":""},{"name":"name","parameters":[{"name":"","type":""}],"returntype":""}]}'
abi = json.loads(abi, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
abi_info = AbiInfo('0x' + addr.to_reverse_hex_str(), 'Main', abi.functions, [])

acc1 = sdk.get_wallet_manager().get_account('ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6', '1')
acc2 = sdk.get_wallet_manager().get_account('AYvTfgEyYduk3zEKMDnZggWQqt9bkASNxJ', '060708')
acc3 = sdk.get_wallet_manager().get_account('AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve', '060708')


class TokenTest(TestCase):
    """
    测试Token合约的功能
    """

    def get_from_hex(self, res):
        """
        hex to string
        :param res:
        :return:
        """
        return util.parse_neo_vm_contract_return_type_string(res)

    def print_info(self, res):
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
        try:
            print('action:%s\nfrom_account:%s\nto_account:%s\namount:%s'
                  % (self.get_from_hex(json_res['Notify'][0]['States'][0]),
                     json_res['Notify'][0]['States'][1], json_res['Notify'][0]['States'][2],
                     util.parse_neo_vm_contract_return_type_integer(json_res['Notify'][0]['States'][3])))
        except Exception:
            print('wrong notify')

    def test_deploy_contract(self):
        tx = sdk.neo_vm().make_deploy_transaction(code, True, 'token_zou', 'v1.0', 'zou', '', 'publish token',
                                             acc1.get_address_base58(), 20000000000, 500)
        sdk.sign_transaction(tx, acc1)
        res = sdk.get_rpc().send_raw_transaction(tx)
        print(res)

    def test_name(self):
        func = abi_info.get_function('name')
        func.set_params_value('a')
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000000, 500, func, True)
        print(self.get_from_hex(res))

    def test_symbol(self):
        func = abi_info.get_function('symbol')
        func.set_params_value('a')
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 2000000, 500, func, True)
        print(util.parse_neo_vm_contract_return_type_string(res))

    def test_total_supply(self):
        func = abi_info.get_function('total_supply')
        func.set_params_value('a')
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000, 500, func, True)
        print(util.parse_neo_vm_contract_return_type_integer(res))

    def test_decimal(self):
        func = abi_info.get_function('decimal')
        func.set_params_value('a')
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000, 500, func, True)
        print(util.parse_neo_vm_contract_return_type_integer(res))

    def test_init(self):
        func = abi_info.get_function('init')
        func.set_params_value('a')
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000, 500, func, False)
        self.print_info(res)

    def test_balance_of(self):
        func = abi_info.get_function('balance_of')
        func.set_params_value(acc1.get_address().to_byte_array())
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000, 500, func, True)
        if res == '':
            print('nothing')
        else:
            print(util.parse_neo_vm_contract_return_type_integer(res))

    def test_transfer(self):
        func = abi_info.get_function('transfer')
        func.set_params_value(acc1.get_address().to_byte_array(), acc3.get_address().to_byte_array(), 900)
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000, 500, func, False)

        self.print_info(res)

    def test_approve(self):
        func = abi_info.get_function('approve')
        func.set_params_value(acc1.get_address().to_byte_array(), acc3.get_address().to_byte_array(), 100)
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000, 500, func, False)

        self.print_info(res)

    def test_transfer_from(self):
        func = abi_info.get_function('transfer_from')
        func.set_params_value(acc3.get_address().to_byte_array(), acc1.get_address().to_byte_array(),
                              acc2.get_address().to_byte_array(), 51)
        res = sdk.neo_vm().send_transaction(contract_addr, acc3, acc3, 200000, 500, func, False)
        self.print_info(res)

    def test_transfer_multi(self):
        """
        func.set_params_value()输入格式需探索
        :return:
        """
        func = abi_info.get_function('transfer_multi')
        func.set_params_value([[acc1.get_address().to_byte_array(), acc2.get_address().to_byte_array(), 10],
                              [acc1.get_address().to_byte_array(), acc3.get_address().to_byte_array(), 10]])
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000, 500, func, False)
        self.print_info(res)

    def test_allowance(self):
        func = abi_info.get_function('allowance')
        func.set_params_value(acc1.get_address().to_byte_array(), acc3.get_address().to_byte_array())
        res = sdk.neo_vm().send_transaction(contract_addr, acc1, acc1, 200000, 500, func, True)
        if res == '':
            print('nothing')
        else:
            print(util.parse_neo_vm_contract_return_type_integer(res))