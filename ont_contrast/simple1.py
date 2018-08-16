# encoding=utf-8
import binascii
import time

import base58

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.wallet.account import AccountData
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.utils import util
from ontology.wallet.wallet_manager import WalletManager
from ontology.ont_sdk import OntologySdk

import base64


private_key = "a350c91744f06d4c9b40c236944aa6ded69e28909d077474e7edebffab7a0315"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"

acc1_address = "AahHajAoNC4MYq15NbLrJfQ6R52FWgkNVR"
acc2_address = "AW6oduZSJef3dtpn8RB5ZmFRBbL9T4AU94"

rpc_address = "http://polaris3.ont.io:20336"

ont = OntologySdk()
ont.get_rpc().set_address(rpc_address)


def get_private_key(key: str, pwd: str, address: str, salt: str, n: int, sig_scheme: SignatureScheme):
    """
    测试如何得到明文私钥：
    :param key:
    :param pwd:
    :param address:
    :param salt:
    :param n:
    :param sig_scheme:
    :return:
    """
    return Account.get_gcm_decoded_private_key(key, pwd, address, base64.b64decode(salt.encode()), n, sig_scheme).hex()


def get_wallet_param_from_prikey(label, prikey, pwd):
    """
    用私钥创建钱包相关参数
    :param label:
    :param prikey:
    :param pwd:
    :return:
    """
    wm = WalletManager()
    acc = wm.create_account_from_prikey(label, pwd, prikey)
    print("salt: " + acc.salt)
    print("address:" + acc.address)
    print("key: " + acc.key)
    print("pubkey: " + acc.publicKey)


def get_storage_value(addr, key):
    return ont.get_rpc().get_storage(addr, key)

def get_balance(addr):
    return ont.get_rpc().get_balance(addr)

if __name__ == '__main__':
    code = "0112c56b6a00527ac46a51527ac46a00c3046a6f696e9c6414006a51c300c36a51c351c37c655b026c7566616a00c30573746172749c640300616a00c3066c697374656e9c640900652c016c7566616a00c30b6765745f616d6f756e74739c6409006572006c7566616a00c30571756572799c645c00681953797374656d2e53746f726167652e476574436f6e74657874616a52527ac46a52c36a51c300c37c681253797374656d2e53746f726167652e476574616a53527ac46a53c30087640900026e6f6c7566616a53c36c756661006c756656c56b659d00631000094e6f742052656164796c756661681953797374656d2e53746f726167652e476574436f6e74657874616a00527ac46a00c307616d6f756e74317c681253797374656d2e53746f726167652e476574616a00c307616d6f756e74327c681253797374656d2e53746f726167652e47657461936a00c307616d6f756e74337c681253797374656d2e53746f726167652e47657461936c75665bc56b681953797374656d2e53746f726167652e476574436f6e74657874616a00527ac46a00c305636f756e747c681253797374656d2e53746f726167652e476574616a51527ac46a00c307616d6f756e74317c681253797374656d2e53746f726167652e476574616a52527ac46a00c307616d6f756e74327c681253797374656d2e53746f726167652e476574616a53527ac46a00c307616d6f756e74337c681253797374656d2e53746f726167652e476574616a54527ac42069735f67616d655f72656164792e3c6c6f63616c733e2e69735f6e756d6265726a55527ac46a51c3539c6422006a55c36a52c36419006a55c36a53c36410006a55c36a54c3640700516c756661006c75660114c56b6a00527ac46a51527ac4c76a52527ac405636f756e746a52c3007bc404616363316a52c3517bc407616d6f756e74316a52c3527bc404616363326a52c3537bc407616d6f756e74326a52c3547bc404616363336a52c3557bc407616d6f756e74336a52c3567bc4681953797374656d2e53746f726167652e476574436f6e74657874616a53527ac46a53c305636f756e747c681253797374656d2e53746f726167652e476574616a54527ac46a54c300876408006a54527ac4616a54c3936a54527ac46a54c353a264200051681553797374656d2e52756e74696d652e4e6f7469667961006c7566616a52c3526a54c3955194c36a55527ac46a52c36a54c35295c36a56527ac46a53c36a55c36a00c35272681253797374656d2e53746f726167652e507574616a53c36a56c36a51c35272681253797374656d2e53746f726167652e507574616a53c305636f756e746a54c35272681253797374656d2e53746f726167652e50757461116a6f696e207375636365737366756c6c79681553797374656d2e52756e74696d652e4e6f7469667961516c7566"
    addr = Address.address_from_vm_code(code)
    print(addr.to_base58())
    print(addr.to_hex_str())
    print(addr.to_reverse_hex_str())
    print(bytes.fromhex("6263635f").decode())


    # res_sc = ont.get_rpc().get_smart_contract_event_by_txhash("d4dbc85999b9ad298d2d2568c085825859ca42b16ffb5ae4a70914724fd400ba")
    # print(res_sc['Notify'][0]['States'])
    #
    # event = ont.get_rpc().get_smart_contract_event_by_txhash("d4dbc85999b9ad298d2d2568c085825859ca42b16ffb5ae4a70914724fd400ba")
    # print(event)
    #
    # code = Address.address_from_vm_code("5cc56b6a00527ac46a51527ac46a00c3046a6f696e9c6414006a51c300c36a51c351c37c65ee016c7566616a00c30573746172749c640300616a00c3066c697374656e9c64090065c5006c7566616a00c30b6765745f616d6f756e74739c640900650b006c756661006c756656c56b659d00631000094e6f742052656164796c756661681953797374656d2e53746f726167652e476574436f6e74657874616a00527ac46a00c307616d6f756e74317c681253797374656d2e53746f726167652e476574616a00c307616d6f756e74327c681253797374656d2e53746f726167652e47657461936a00c307616d6f756e74337c681253797374656d2e53746f726167652e47657461936c75665bc56b681953797374656d2e53746f726167652e476574436f6e74657874616a00527ac46a00c305636f756e747c681253797374656d2e53746f726167652e476574616a51527ac46a00c307616d6f756e74317c681253797374656d2e53746f726167652e476574616a52527ac46a00c307616d6f756e74327c681253797374656d2e53746f726167652e476574616a53527ac46a00c307616d6f756e74337c681253797374656d2e53746f726167652e476574616a54527ac42069735f67616d655f72656164792e3c6c6f63616c733e2e69735f6e756d6265726a55527ac46a51c3536a55c36a52c3846a55c36a53c3846a55c36a54c38487640700516c756661006c75660111c56b6a00527ac46a51527ac4681953797374656d2e53746f726167652e476574436f6e74657874616a52527ac46a52c305636f756e747c681253797374656d2e53746f726167652e476574616a53527ac46a53c30087640900006a53527ac4616a53c351936a53527ac46a53c353a26329006a52c3036163636a53c3937c681253797374656d2e53746f726167652e47657461009e642200610131681553797374656d2e52756e74696d652e4e6f7469667961006c7566616a52c3036163636a53c3936a00c35272681253797374656d2e53746f726167652e507574616a52c306616d6f756e746a53c3936a51c35272681253797374656d2e53746f726167652e507574616a52c305636f756e746a53c35272681253797374656d2e53746f726167652e507574610130681553797374656d2e52756e74696d652e4e6f7469667961516c7566")
    #
    # res = ont.get_rpc().get_storage("cfd1491f7ff635a67c9488fbba5b5636f1df3d07", "acc1".encode().hex())
    # print(res)

    # barr = bytearray("AFmseVrdL9f9oyCzZefL9tG6UbvhUMqNMV", encoding="utf-8")
    # a = ""
    # for i in barr:
    #     a += str(int(i)) + ','
    #
    # print(a)


    # code = "0111c56b6a00527ac46a51527ac46a00c3036765749c648600681953797374656d2e53746f726167652e476574436f6e74657874616a52527ac46a52c36a51c37c681253797374656d2e53746f726167652e476574616a53527ac409323333333333333333681253797374656d2e52756e74696d652e4c6f67610340e201681553797374656d2e52756e74696d652e4e6f74696679616a53c36c7566616a00c3037075749c649e00681953797374656d2e53746f726167652e476574436f6e74657874616a52527ac46a52c36a51c3681b53797374656d2e426c6f636b636861696e2e476574486569676874615272681253797374656d2e53746f726167652e5075746109323333333333333333681253797374656d2e52756e74696d652e4c6f67610340e201681553797374656d2e52756e74696d652e4e6f7469667961516c756661006c7566"
    # code_addr = Address.address_from_vm_code(code)

    # bytearray1 = bytearray([ 2, 123, 48, 51, 62, 13, 14, 101, 82, 174, 109, 29, 169, 249, 64, 159, 85, 30, 53, 238, 151, 25, 48, 94, 148, 93, 196, 220, 186, 153, 132, 86, 202 ])
    # a = Address.address_from_bytes_pubkey(bytes(bytearray1))
    # print(a.to_base58())
    #
    # addr = Address.address_from_vm_code("57c56b6101646c766b00527ac4546153c66c766b527a527ac46c766b54c36122414e4835624872727431313158774e456e75505a6a36753935446436753747344436007cc46c766b54c3612241597654666745795964756b337a454b4d446e5a67675751717439626b41534e784a517cc46c766b54c36c766b00c3527cc46c766b54c36c766b51527ac451c56c766b52527ac46c766b52c3006c766b51c3c4006122416562757655615a516347586d474a54515063586d484c6438383842736358555946087472616e736665726c766b52c361537951795572755172755279527954727552727568164f6e746f6c6f67792e4e61746976652e496e766f6b656c766b53527ac46c766b53c300517f519c009c6c766b55527ac46c766b55c3640f0061006c766b56527ac4620f0061516c766b56527ac46203006c766b56c3616c7566")
    # print(addr.to_base58())
    # print(code_addr.to_base58())
    #
    # contract_addr = code_addr.to_array()
    #
    # print(base58.b58encode(contract_addr).decode('utf-8'))
    # print("ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6")

    # get_wallet_param_from_prikey("polaris_acc1", util.hex_to_bytes(private_key2), "060708")
    # print(type(get_storage_value("0e7c864aa088837a7348eb04ce1b70120be4ea1d", "zouxueyan")))
    # print(get_balance(addr=acc1_address))

    # print(ont.rpc.get_smart_contract("0e7c864aa088837a7348eb04ce1b70120be4ea1d"))

    # wm = ont.get_wallet_manager()
    # wm.open_wallet("/Users/zou/PycharmProjects/ont_test/ont_contrast/wallet.json")
    #
    # addr1 = "ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6"
    # addr2 = "AYvTfgEyYduk3zEKMDnZggWQqt9bkASNxJ"
    # private_key1 = get_private_key("mWDJbkVESLBxUmwbcX9ZeMncRvmba8sx3YOejn5C0g22vvzubda6qMh4rkFu0N90", "1", addr1,
    #                                "NgNnWTOJ0KlzfjRBhK1vIg==", 16384, SignatureScheme.SHA256withECDSA)
    # private_key2 = get_private_key("TbQ4BeALgaw5kKum3AthaTMyaQ5rabWvdrmhTaYZQElM28cYpeZqx5g2N7kJj3+a", "060708", addr2,
    #                                "2sxp7j+E8c3MFDaAf+0YNQ==", 16384, SignatureScheme.SHA256withECDSA)
    # acc1 = Account(util.hex_to_bytes("523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"), SignatureScheme.SHA256withECDSA)
    # acc2 = Account(util.hex_to_bytes("75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"), SignatureScheme.SHA256withECDSA)
    # acc3 = Account(util.hex_to_bytes("1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"), SignatureScheme.SHA256withECDSA)
    #
    #
    # pub_keys = [acc1.get_public_key(), acc2.get_public_key(), acc3.get_public_key()]
    #
    # multi_addr = Address.address_from_multi_pubKeys(2, pub_keys)
    #
    # tx = ont.native_vm().asset().new_transfer_transaction("ont", acc1.get_address_base58(), multi_addr.to_base58(), 1,
    #                                                  acc1.get_address_base58(), 20000, 500)
    #
    # ont.add_sign_transaction(tx, acc1)
    # txid = ont.get_rpc().send_raw_transaction(tx)
    #
    # print("txid1: " + txid)

    # mul_tx = ont.native_vm().asset().new_transfer_transaction("ont", multi_addr.to_base58(), acc2.get_address_base58(),
    #                                                           1, acc2.get_address_base58(), 20000, 500)
    #
    # ont.add_sign_transaction(mul_tx, acc2)
    #
    # ont.add_multi_sign_transaction(mul_tx, 2, pub_keys, acc1)
    # ont.add_multi_sign_transaction(mul_tx, 2, pub_keys, acc2)
    #
    # txid = ont.rpc.send_raw_transaction(mul_tx)
    #
    # print("txid " + txid)
    #
    # print(multi_addr.to_hex_string())
    # print(multi_addr.to_base58())

    # tx = ont.native_vm().asset().new_transfer_transaction("ont", addr1, addr2, 1, addr1, 20000000, 500)
    # ont.sign_transaction(tx, acc1)
    # ont.add_sign_transaction(tx, acc2)
    # res = ont.get_rpc().send_raw_transaction(tx)
    # if len(res) != 64:
    #     raise Exception(res)
    #
    # print(len(res))

    # print(str(binascii.b2a_hex("48656c6c6f".encode())))