#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/1 13:33
# @Author  : 0x00006913
# @Site    :
# @File    : eth_client.py
import json
import time
from web3.exceptions import TransactionNotFound
from defaults import conf_for_name
from web3 import Web3
import eth_utils
from web3 import WebsocketProvider
from web3 import HTTPProvider
from decimal import Decimal
import requests


class TransactionRet():

    def __init__(self, tran_hash: str, web3: Web3):
        self._web3 = web3;
        self.tran_hash = tran_hash;

    def wait(self, timeout=60, interval=2) -> dict:
        end_time = time.time() + timeout * 1_000
        while time.time() < end_time:
            try:
                return self._web3.eth.getTransactionReceipt(self.tran_hash)
            except TransactionNotFound:
                time.sleep(interval)

        raise TransactionNotFound("timeout and can not find the transaction")


class EthClient(object):

    def __init__(self, network: str, protocol: str = 'http'):
        self.conf = conf_for_name(network)
        if protocol == 'websocket':
            provider = WebsocketProvider(self.conf['websocket'])
        else:
            provider = HTTPProvider(self.conf['http'])
        self.web3 = Web3(provider=provider)
        self.chain_id = self.web3.eth.chainId;
        self.symbol = self.conf['symbol']

    def to_human_num(self, num):
        return eth_utils.from_wei(number=num, unit="ether")

    def get_balance_in_human(self, address: str):
        return eth_utils.from_wei(number=self.get_balance(address), unit="ether")

    def get_balance(self, address: str) -> Decimal:
        """
        获取账户的eth余额,单位是wei
        :param address:
        :return:
        """
        return self.web3.eth.getBalance(address)

    def transfer_eth(self, from_address: str, private_key: str, to_address: str, amount: int, gas_price: float,
                     gas_limit: int = 21000):
        """
        eth转账
        :param private_key:
        :param to_address:
        :param amount:
        :param gas_limit:
        :return:
        """
        signed_tran = self.web3.eth.account.sign_transaction({
            'from': from_address,
            'to': to_address,
            'value': amount,
            'gas': gas_limit,
            'gasPrice': eth_utils.to_wei(gas_price, "gwei"),
            'nonce': self.web3.eth.getTransactionCount(from_address),
            'chainId': self.chain_id
        }, private_key=private_key)

        tran_hash = self.web3.eth.sendRawTransaction(signed_tran.rawTransaction)
        return TransactionRet(tran_hash=tran_hash, web3=self.web3)

    def __get_abi(self, contract_address: str):
        rsp = requests.get(self.conf.get("etherscan"),
                           {"action": "getabi", "module": "contract", "address": contract_address})
        if rsp.status_code == 200:
            return rsp.json()['result']

    def get_safe_gas_price(self, default_value):
        """
        获取最保险最经济的gas价格
        :return:
        """
        headers = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
        ts = str(int(time.time()));
        rsp = requests.get(url=self.conf.get("etherscan") + "&ts=" + ts, params=
        {"action": "gasoracle", "module": "gastracker" }, headers=headers);

        if rsp.status_code == 200:
            return int(rsp.json()['result']['SafeGasPrice'])
        print("@@get_safe_gas_price, error=", rsp.status_code)
        return default_value;

    def get_safe_gas_price_until(self, max_price, print_log: bool = False):
        """获取最优惠的价格，不断的尝试"""
        price = self.get_safe_gas_price(max_price + 1)
        while price > max_price:
            time.sleep(3)
            price = self.get_safe_gas_price(max_price + 1)
            if print_log:
                logtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print("%s-正在等待gas费用降低。当前费用：%d" % (logtime, price))
        return price


if __name__ == '__main__':
    client = EthClient(network="bsc-test")


