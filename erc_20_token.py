#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/1 18:19
# @Author  : 0x00006913
# @Site    :
# @File    : erc_20_token.py
import json

from web3 import Web3
from web3.contract import ConciseContract
from decimal import Decimal
from eth_client import EthClient
import eth_utils
from eth_client import TransactionRet


class Erc20Token():
    EIP20_ABI = json.loads(
        '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501

    def __init__(self, contract_address: str, web3: Web3):
        self.contract_address = Web3.toChecksumAddress(contract_address);
        self._web3 = web3;
        self.contract = self._web3.eth.contract(address=self.contract_address, abi=Erc20Token.EIP20_ABI)
        self.symbol = self.contract.caller().symbol()
        self.precision = 10 ** int(self.contract.caller().decimals())
        self.token_balance = self.balanceOf(self.contract_address)
        self.chain_id = self._web3.eth.chainId

    def inHumanNum(self, amount:Decimal):
        return amount / self.precision

    def balanceOfInHuman(self, address: str):
        return self.inHumanNum(self.contract.caller().balanceOf(address))

    def balanceOf(self, address: str):
        return self.contract.caller().balanceOf(address);

    def transfer(self, from_address: str, private_key: str, to_address: str, amount, gas_price: float,
                 gas_limit: int = 21000):
        txn = {
            'chainId': self.chain_id,
            'gas': gas_limit,
            'gasPrice': eth_utils.to_wei(gas_price, "gwei"),
            'nonce': self._web3.eth.getTransactionCount(from_address),
            'from': from_address
        }
        transfer_txn = self.contract.functions.transfer(to_address, int(amount)).buildTransaction(txn)

        signed_tran = self._web3.eth.account.sign_transaction(transfer_txn, private_key=private_key)
        tran_hash = self._web3.eth.sendRawTransaction(signed_tran.rawTransaction)
        return TransactionRet(tran_hash=tran_hash, web3=self._web3)


if __name__ == '__main__':
    pass
