from unittest import TestCase
from ont_contrast.demo.cli.demo_cli import DemoClient

client = DemoClient("http://polaris3.ont.io:20336", "wallet.json", True, ["1", "060708", "060708"],
                    "/Users/zou/PycharmProjects/ont_test/ont_contrast/demo/cli/demo.avm",
                    "/Users/zou/PycharmProjects/ont_test/ont_contrast/demo/cli/abi.json")


class TestDemoCli(TestCase):

    def test_start_game(self):
        """
        测试场景：start_game方法，部署合约
        预期结果：调用成功，并返回交易id
        问题记录：1 钱包格式 2 sdk更新
        实际结果：e7f77cd216b1da549b61003186b485f6743a2f95ffc66e13c720de64466a615f
        :return:
        """
        print(client.start_game(2))

    def test_join(self):
        """
        测试场景：join方法，调用合约特定方法
        预期结果：调用成功，并进入循环，直到game ready
        实际结果：
        :return:
        """
        client.join_game(1, 2)