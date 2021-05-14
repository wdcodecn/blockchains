#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/5 01:46
# @Author  : 0x00006913
# @Site    : 
# @File    : create_wallets.py
import argparse
from configparser import ConfigParser
from erc_20_token import Erc20Token
import os
import traceback
from wallet import Wallet
from eth_client import EthClient
import eth_utils
from web3 import Web3
from eth_account import Account

parser = argparse.ArgumentParser()

parser.add_argument(
    "--wallet-file",
    type=str,
    default="wallet.txt",
    help="子钱包的文件.")

parser.add_argument(
    "--num",
    type=int,
    default=1,
    help="数量")

argv = parser.parse_args()
with open(argv.wallet_file,'a+') as f:
    for i in range(0,argv.num):
        wallet = Account.create();
        privateKey = wallet._key_obj
        publicKey = privateKey.public_key
        address = publicKey.to_checksum_address()
        f.write(str(privateKey)+" "+ address + "\n")
