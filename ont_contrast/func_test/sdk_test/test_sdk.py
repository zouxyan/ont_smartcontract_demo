from ontology.ont_sdk import OntologySdk
from ontology.account.account import Address
from ontology.utils import util
from unittest import TestCase

import time

# -------------------------------------------
# GLOBAL SETTINGS
# -------------------------------------------
rpc_addr = 'http://polaris3.ont.io:20336'
sdk = OntologySdk()
sdk.set_rpc(rpc_addr)
sdk.open_wallet('/Users/zou/PycharmProjects/ont_test/ont_contrast/demo/cli/wallet.json')

acc1 = sdk.get_wallet_manager().get_account('ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6', '1')
acc2 = sdk.get_wallet_manager().get_account('AYvTfgEyYduk3zEKMDnZggWQqt9bkASNxJ', '060708')
acc3 = sdk.get_wallet_manager().get_account('AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve', '060708')

pub_keys = [acc1.get_public_key(), acc2.get_public_key(), acc3.get_public_key()]
multi_addr = Address.address_from_multi_pubKeys(2, pub_keys)


class TestSDK(TestCase):
    def test_multi_sig_transaction(self):
        print('账户1余额：%s' %sdk.get_rpc().get_balance(acc1.get_address_base58())['ont'])
        tx = sdk.native_vm().asset().new_transfer_transaction("ont", acc1.get_address_base58(), multi_addr.b58encode(),
                                                              100, acc1.get_address_base58(), 200000, 500)
        sdk.add_sign_transaction(tx, acc1)
        txid = sdk.get_rpc().send_raw_transaction(tx)
        time.sleep(2)
        print('账户1给多签地址打钱，交易ID：%s' %txid)
        balance_acc1 = sdk.get_rpc().get_balance(acc1.get_address_base58())
        balance_multi = sdk.get_rpc().get_balance(multi_addr.b58encode())
        print('账户1余额：%s 多签地址余额：%s' %(balance_acc1['ont'], balance_multi['ont']))

        tx = sdk.native_vm().asset().new_transfer_transaction('ont', multi_addr.b58encode(), acc1.get_address_base58(),
                                                              50, acc1.get_address_base58(), 200000, 500)
        sdk.sign_transaction(tx, acc1)
        sdk.add_multi_sign_transaction(tx, 2, pub_keys, acc1)
        sdk.add_multi_sign_transaction(tx, 2, pub_keys, acc2)
        txid = sdk.get_rpc().send_raw_transaction(tx)
        time.sleep(2)
        print('多签地址给acc1打钱，交易ID：%s' % txid)
        balance_acc1 = sdk.get_rpc().get_balance(acc1.get_address_base58())
        balance_multi = sdk.get_rpc().get_balance(multi_addr.b58encode())
        print('账户1余额：%s 多签地址余额：%s' % (balance_acc1['ont'], balance_multi['ont']))

    # def test_