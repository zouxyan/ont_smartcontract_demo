# coding=utf-8
import base64
import json
import time

from collections import namedtuple
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.wallet.account import AccountData
from ontology.common.address import Address


# rpc_addr = "http://polaris3.ont.io:20336"


class DemoClient(object):
    """

    """

    def __init__(self, rpc_addr: str, wallet_file: str, is_maker: bool, pwd, avm_file, abi_file):
        self.sdk = OntologySdk()
        self.sdk.rpc.set_address(rpc_addr)
        self.sdk.open_wallet(wallet_file)
        self.is_maker = is_maker  # 可以查询一个合约存不存在，存在就可以让maker是True，而不必自己指定了
        # self.code = None
        # self.contract_addr = None
        # self.code_addr = None
        # self.contract_acc = None
        self.__pwd = pwd

        self.__get_code_from_avm(avm_file)
        self.__get_abi_from_file(abi_file)

    @staticmethod
    def is_transaction_success(txid):
        if len(txid) != 64:
            return False
        return True

    def start_game(self, acc_index):
        if not self.is_maker:
            return
        acc = self.get_account_by_index(acc_index)
        txid = self.deploy_contract(need_storage=True, name="sixsixsix", code_ver="1.0", author="tomzou",
                                    email="tomzou@blackfish.cn", desp="demo", acc=acc, gas_limit=20200000, gas_price=500)
        if not self.is_transaction_success(txid):
            raise Exception(txid)
        return txid

    def get_account_by_index(self, acc_index):
        wm = self.sdk.get_wallet_manager()
        return wm.get_account(wm.get_wallet().get_account_by_index(acc_index).get_address(), self.__pwd[acc_index])

    def deploy_contract(self, need_storage, name, code_ver, author, email, desp, acc, gas_limit, gas_price):
        tx = self.sdk.neo_vm().make_deploy_transaction(self.code, need_storage=need_storage, name=name,
                                                       code_version=code_ver, author=author, email=email, desp=desp,
                                                       payer=acc.get_address_base58(), gas_limit=gas_limit, gas_price=gas_price)
        self.sdk.sign_transaction(tx, acc)
        return self.sdk.get_rpc().send_raw_transaction(tx)

    def __get_code_from_avm(self, avm_file):
        f = open(avm_file)
        self.code = f.readline()
        code_addr_obj = Address.address_from_vm_code(self.code)
        self.code_addr = code_addr_obj.to_reverse_hex_str()
        self.contract_acc = code_addr_obj.to_base58()
        self.contract_addr = code_addr_obj.to_byte_array()
        f.close()

    def __get_abi_from_file(self, abi_file):
        f = open(abi_file)
        abi_str = f.readline()
        abi = json.loads(abi_str, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self.abi_info = AbiInfo("0x" + self.code_addr, "main", abi.functions, [])

    def join_game(self, amount, acc_index):
        acc = self.get_account_by_index(acc_index)

        # 调用相应的函数，需写完合约再回头搞
        func_join = self.abi_info.get_function("join")
        func_join.set_params_value(acc.get_address_base58(), amount)
        func_read_res = self.abi_info.get_function("is_game_ready")

        txid = self.sdk.neo_vm().send_transaction(self.contract_addr, acc, acc, 2000000, 500, func_join, False)

        print(txid)
        if not self.is_transaction_success(txid):
            raise Exception(txid)

        tx_info = self.sdk.get_rpc().get_raw_transaction(txid)#
        while tx_info == 'unknown transaction' or tx_info is None:
            tx_info = self.sdk.get_rpc().get_smart_contract_event_by_txhash(txid)
            # here: tx_info很奇怪，记得回来看
        try:
            notify_info = tx_info['Notify'][0]['States']
        except Exception:
            raise Exception(tx_info)

        print(notify_info)
        if notify_info == '4e6f206d6f72652073656174':
            raise Exception("No more seat")
        elif notify_info == '6a6f696e207375636365737366756c6c79':
            # 等待游戏结束，不停滴向合约pull结果
            while True:
                time.sleep(1)
                res = self.sdk.neo_vm().send_transaction(self.contract_addr, acc, acc, 2000000, 500, func_read_res, True)
                if res is True:
                    print(res)
                    break
