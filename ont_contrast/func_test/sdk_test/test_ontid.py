from ontology.ont_sdk import OntologySdk
from ontology.account.account import Address
from ontology.utils import util
from unittest import TestCase

import time

# -------------------------------------------
# GLOBAL SETTINGS
# -------------------------------------------
# rpc_addr = 'http://10.32.16.26:20336'
rpc_addr = "http://polaris3.ont.io:20336"
sdk = OntologySdk()
sdk.set_rpc(rpc_addr)
sdk.open_wallet('/Users/zou/PycharmProjects/ont_test/ont_contrast/demo/cli/wallet.json')

acc1 = sdk.get_wallet_manager().get_account('ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6', '1')
acc2 = sdk.get_wallet_manager().get_account('AYvTfgEyYduk3zEKMDnZggWQqt9bkASNxJ', '060708')
acc2.get_public_key()
acc3 = sdk.get_wallet_manager().get_account('AazEvfQPcQ2GEFFPLF1ZLwQ7K5jDn81hve', '060708')

did = 'did:ont:' + acc1.get_address_base58()


class TestOntid(TestCase):
    def test_new_registry_ontid_transaction(self):
        tx = sdk.native_vm().ont_id().new_registry_ontid_transaction(did, acc2.get_public_key(), acc1.get_address_base58(),
                                                                200000, 500)
        sdk.sign_transaction(tx, acc2)
        sdk.add_sign_transaction(tx, acc1)
        tx = sdk.get_rpc().send_raw_transaction(tx)
        print(tx)

    def test_new_get_ddo(self):
        tx = sdk.native_vm().ont_id().new_get_ddo_transaction(did)
        out_ddo = sdk.rpc.send_raw_transaction_pre_exec(tx)
        parsed_ddo = sdk.native_vm().ont_id().parse_ddo(did, out_ddo)
        print(parsed_ddo)

    def test_new_add_attribute_transaction(self):
        attris = []
        attri1 = {}
        attri1["key"] = "xue"
        attri1["type"] = "intern"
        attri1["value"] = "fat boy"

        attris.append(attri1)

        tx = sdk.native_vm().ont_id().new_add_attribute_transaction(did, acc2.get_public_key(), attris,
                                                                    acc1.get_address_base58(), 20000,
                                                                    500)
        tx = sdk.sign_transaction(tx, acc1)
        tx = sdk.add_sign_transaction(tx, acc1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        print(tx_hash)

    def test_new_remove_attribute_transaction(self):
        tx = sdk.native_vm().ont_id().new_remove_attribute_transaction(did, acc1.get_public_key(), "key2",
                                                                       acc1.get_address_base58(), 20000, 500)
        tx = sdk.sign_transaction(tx, acc1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)

    def test_new_add_pubkey_transaction(self):
        tx = sdk.native_vm().ont_id().new_add_pubkey_transaction(did, acc2.get_public_key(), acc1.get_public_key(),
                                                                 acc1.get_address_base58(), 20000,
                                                                 500)
        tx = sdk.sign_transaction(tx, acc1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        print(tx_hash)

    def test_new_remove_pubkey_transaction(self):
        tx = sdk.native_vm().ont_id().new_remove_pubkey_transaction(did, acc1.get_public_key(), b'131402c06c72787291a7ce27be41ce569b42abd5824d2a93158ec3c49575d1ae9e37c7',
                                                                    acc1.get_address_base58(), 20000,
                                                                    500)
        tx = sdk.sign_transaction(tx, acc1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        print(tx_hash)

    def test_new_add_recovery_transaction(self):
        tx = sdk.native_vm().ont_id().new_add_rcovery_transaction(did, acc2.get_public_key(), acc1.get_address_base58(),
                                                                  acc1.get_address_base58(), 20000,
                                                                  500)
        sdk.sign_transaction(tx, acc2)
        sdk.add_sign_transaction(tx, acc1)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        print(tx_hash)
