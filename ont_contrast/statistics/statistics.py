from ontology.ont_sdk import OntologySdk
from unittest import TestCase

import time

rpc_addr = 'http://10.32.16.26:20336'
sdk = OntologySdk()
sdk.set_rpc(rpc_addr)
sdk.open_wallet('/Users/zou/PycharmProjects/ont_test/ont_contrast/demo/cli/wallet.json')


class Statistics(TestCase):
    def test_average_block_generate_time(self):
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

    def test_average_tx_per_block(self):
        len_sum = 0.0
        curr_height = sdk.get_rpc().get_block_count() - 1
        for i in range(100):
            len_sum += len(sdk.get_rpc().get_block_by_height(curr_height - i)['Transactions'])
        print(len_sum / 100)

