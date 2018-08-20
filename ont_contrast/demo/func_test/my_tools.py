from ontology.account.account import Address
from ontology.wallet.account import AccountData
from ontology.ont_sdk import OntologySdk

"""
包含一些字节 string转换之类
"""

sdk = OntologySdk()
sdk.set_rpc('http://polaris3.ont.io:20336')
sdk.open_wallet('/Users/zou/PycharmProjects/ont_test/ont_contrast/demo/cli/wallet.json')


def get_bytearray_addr(addr_base58, pwd):
    acc = sdk.get_wallet_manager().get_account(addr_base58, pwd)
    return acc.get_address().to_array()


def get_bytes_addr(index):
    acc: AccountData = sdk.get_wallet_manager().get_wallet().get_account_by_index(index)
    print(acc.address)
    acc = sdk.get_wallet_manager().get_account()


def get_val_from_bytes(byte_arr):
    arr = [x for x in byte_arr]
    str_val = ''
    for x in arr:
        str_val += "\\" + hex(x)[1:]
    return str_val


if __name__ == '__main__':
    # aa = get_bytearray_addr('ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6', '1')
    # print(len(aa))
    # print(aa)
    byte_arr = get_bytearray_addr('ANH5bHrrt111XwNEnuPZj6u95Dd6u7G4D6', '1')
    print(byte_arr)
    print(get_val_from_bytes(byte_arr))
