#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/1 13:32
# @Author  : 0x00006913
# @Site    : 
# @File    : wallet.py
from eth_keys import keys
from hexbytes import HexBytes
from eth_client import EthClient


class Wallet(object):

    def __init__(self, address: str, private_key: str, eth_client: EthClient = EthClient(network="mainnet")):
        self.address = address;
        self.private_key = private_key;
        self.eth_client = eth_client;

    @staticmethod
    def from_private_key(private_key: str):
        pr_key = keys.PrivateKey(HexBytes.fromhex(private_key))
        return Wallet(pr_key.public_key.to_address(), private_key)

    def transfer_eth(self, to_address: str, amount: float, gas_price:float ,gas_limit: int = 21000) -> bool:
        import eth_utils
        amount_wei= eth_utils.to_wei(number=amount, unit="ether")
        ret = self.eth_client.transfer_eth(from_address=self.address, private_key=self.private_key,
                                           to_address=to_address,
                                           amount=amount_wei, gas_limit=gas_limit ,gas_price=gas_price)
        tran_ret = ret.wait()
        return tran_ret


