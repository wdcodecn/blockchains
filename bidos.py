
# coding=UTF-8
# This Python file uses the following encoding: utf-8

import argparse
import time

from web3 import Web3

from eth_client import EthClient
from configparser import ConfigParser

parser = argparse.ArgumentParser()

cfg = ConfigParser()
cfg.read("app.ini")
privateKey = cfg.get('main', 'privateKey')
address = cfg.get('main', 'address')

print("读取账户成功:", address)
ethClient = EthClient(network="bsc")

bidos_addr = "0x6Ea4fd26f9E0Ba1BCAc8519Bd7D69296e32F9157"


parser.add_argument(
    "--count",
    type=int,
    default=10,
    help="执行次数")


parser.add_argument(
    "--gas-price",
    type=int,
    default=5,
    help="指定每次交易的gas价格，价格越高越容易成交")


parser.add_argument(
    "--gas-limit",
    type=int,
    default=200000,
    help="指定每次交易需要的gas，默认是59136")

argv = parser.parse_args()

gasPriceWei = argv.gas_price;
gasLimit = argv.gas_limit;


for i in range(0, argv.count):
    try:
        tran = ethClient.transfer_eth(from_address=address, private_key=privateKey,
                                      to_address=Web3.toChecksumAddress(bidos_addr),
                                      amount=0,
                                      gas_price=gasPriceWei,
                                      gas_limit=gasLimit)
        # print(tran.wait());
        time.sleep(2);
    except:
        print("错误了...")
        time.sleep(2);
