from ontology.ont_sdk import OntologySdk
from ontology.account.account import Address, Account
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.utils import util
from unittest import TestCase
from collections import namedtuple

import time
import math
import json

rpc_addr = 'http://polaris3.ont.io:20336'
sdk = OntologySdk()
sdk.set_rpc(rpc_addr)
sdk.open_wallet('/Users/zou/PycharmProjects/ont_test/ont_contrast/demo/cli/wallet.json')


if __name__ == '__main__':
    time_list = []
    now_count = sdk.get_rpc().get_block_count()
    now = time.time()
    for i in range(11):
        print('%f: %d' %(now, now_count))
        while True:
            new_count = sdk.get_rpc().get_block_count()
            if new_count > now_count:
                curr_time = time.time()
                time_list.append(curr_time - now)
                now = curr_time
                now_count = new_count
                break
            time.sleep(0.1)
    print(sum(time_list[1:]) / 10)