#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/1 20:48
# @Author  : 0x00006913
# @Site    : 
# @File    : app.py
import argparse
import time
from configparser import ConfigParser
from decimal import Decimal

from erc_20_token import Erc20Token
import os
import traceback
from wallet import Wallet
from eth_client import EthClient
import eth_utils
from web3 import Web3

parser = argparse.ArgumentParser()

parser.add_argument(
    'command',
    help="指定的执行的指令，transfer_eth_to_wallets.. 等\n"
)

parser.add_argument(
    "--config",
    type=str,
    default="app.ini",
    help="配置文件")

parser.add_argument(
    "--network",
    type=str,
    default="mainnet",
    help="网络")

parser.add_argument(
    "--wallet-file",
    type=str,
    default="wallet.txt",
    help="子钱包的文件.")

parser.add_argument(
    "--eth-amount",
    type=float,
    default=1,
    help="给子账户转账的ETH数量")

parser.add_argument(
    "--gas",
    type=int,
    default=21000,
    help="指定每次交易需要的gas，默认是21000")

parser.add_argument(
    "--gas-price",
    type=int,
    help="指定每次交易的gas价格，价格越高越容易成交")

parser.add_argument(
    "--max-gas-price",
    type=int,
    help="指定最大的交易gas价格，会根据gas orcale匹配当前最划算的gas。 如果超出了则继续等待到合适的价格")

parser.add_argument(
    "--erc20-contract",
    type=str,
    help="erc20代币的合约地址.")

parser.add_argument(
    "--gas-price-add",
    type=int,
    default=1,
    help="在现有的gas价格指定增加价格")

argv = parser.parse_args()
command = argv.command

client = EthClient(network=argv.network)


def readWalletsFromFile(file):
    wallets = []
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            pair = line.replace("\n", "").split(" ")
            wallets.append(Wallet(Web3.toChecksumAddress(pair[1]), pair[0], eth_client=client))
    return wallets


def loadMainWallet(config):
    """
    读取主账户的配置
    :return:
    """
    cfg = ConfigParser()
    cfg.read(config)
    privateKey = cfg.get('main', 'privateKey')
    address = cfg.get('main', 'address')
    mainWallet = Wallet(address=Web3.toChecksumAddress(address), private_key=privateKey, eth_client=client)
    print("读取配置成功....")
    print("主账号为:", address)
    return mainWallet


def _clearProgress(command):
    file = "./data/" + command + ".txt"
    if os.path.exists(file):
        os.remove(file)


def _saveProgress(command, lastAddress):
    with open("./data/" + command + ".txt", 'w') as f:
        f.write(lastAddress)


def _readProgress(command):
    file = "./data/" + command + ".txt"
    if not os.path.exists(file):
        return None

    with open(file, 'r') as f:
        return f.readline()


def readTaskAndProgress():
    lastAddress = _readProgress(command)
    wallets = readWalletsFromFile(argv.wallet_file)
    totalSize = len(wallets)
    if lastAddress is not None:
        print("发现未完成的任务，最后的账户为:", lastAddress)
        for wallet in wallets:
            if wallet.address != lastAddress:
                wallets.remove(wallet)
            else:
                wallets.remove(wallet)
                break
    return wallets, lastAddress, totalSize


def transfer_eth_to_wallets():
    mainWallet = loadMainWallet(argv.config)
    gas = argv.gas
    assert argv.gas_price is not None, "--gas-price 参数不能为空"
    gas_price = argv.gas_price

    wallets, lastAddress, totalSize = readTaskAndProgress()
    try:
        print("开始给%d个账户转账, 剩余%d个账户" % (totalSize, len(wallets)))
        for wallet in wallets:
            ret = mainWallet.transfer_eth(wallet.address, argv.eth_amount, gas_limit=gas, gas_price=gas_price)
            lastAddress = wallet.address
            print(wallet.address, ret['transactionHash'].hex())

    except:
        traceback.print_exc()
        if lastAddress is not None:
            _saveProgress(command, lastAddress)

    print("转账任务结束.....")
    _clearProgress(command)


def collect_erc20_token():
    assert argv.erc20_contract is not None, "--erc20-contract 参数不能为空"
    mainWallet = loadMainWallet(argv.config)
    wallets, lastAddress, totalSize = readTaskAndProgress()
    trc20Token = Erc20Token(argv.erc20_contract, web3=client.web3)
    gas = argv.gas
    assert not (argv.gas_price is None and argv.max_gas_price is None), "--gas-price 和 --max-gas-price 必须设置一个"
    gas_price = argv.gas_price
    if argv.max_gas_price is not None:
        print("启用智能GAS调整逻辑，程序会获取当前网络的最优Gas费用，在次基础上加上3，作为本次交易的gas费用")
        gas_price = client.get_safe_gas_price_until(argv.max_gas_price,True) + argv.gas_price_add

    try:
        print("开始归集%d个账户, 剩余%d个账户" % (totalSize, len(wallets)))
        for wallet in wallets:
            balance = trc20Token.balanceOf(wallet.address)
            if balance > 0.001 * trc20Token.precision:
                if argv.max_gas_price is not None:
                    gas_price = client.get_safe_gas_price_until(argv.max_gas_price, True) + 3
                txn = trc20Token.transfer(from_address=wallet.address, private_key=wallet.private_key,
                                          to_address=mainWallet.address, amount=balance, gas_limit=gas,
                                          gas_price=gas_price)
                print(wallet.address,txn.tran_hash.hex())
                time.sleep(2)
                # result = txn.wait(timeout=5 * 60)
                # status = result['status']
                # txnId = result['transactionHash'].hex()
                # print("账户%s, 余额: %s %s , 成功:%s, 交易ID=%s" % (
                #     wallet.address, trc20Token.inHumanNum(balance), trc20Token.symbol, str(status), txnId))
            else:
                print("账户%s ,余额为0 %s" % (wallet.address, trc20Token.symbol))

            lastAddress = wallet.address
    except:
        traceback.print_exc()
        if lastAddress is not None:
            _saveProgress(command, lastAddress)


def collect_eth():
    mainWallet = loadMainWallet(argv.config)
    wallets, lastAddress, totalSize = readTaskAndProgress()
    gas = argv.gas
    assert not (argv.gas_price is None and argv.max_gas_price is None), "--gas-price 和 --max-gas-price 必须设置一个"
    gas_price = argv.gas_price
    if argv.max_gas_price is not None:
        print("启用智能GAS调整逻辑，程序会获取当前网络的最优Gas费用，在次基础上加上3，作为本次交易的gas费用")
        gas_price = client.get_safe_gas_price(argv.max_gas_price);
    try:
        print("开始归集%d个账户, 剩余%d个账户，gas_limit=%d, gas_price=%d" % (totalSize, len(wallets), gas, gas_price))
        for wallet in wallets:
            balance = client.get_balance(wallet.address)
            print("账户%s, 余额: %s ETH" % (wallet.address, client.to_human_num(balance)))
            gasPriceWei = eth_utils.to_wei(gas_price, "gwei")
            gasWei = gas * gasPriceWei
            if balance - gasWei > 0:
                if argv.max_gas_price is not None:
                    gas_price = client.get_safe_gas_price_until(argv.max_gas_price, True) + 3

                txn = client.transfer_eth(from_address=wallet.address, private_key=wallet.private_key,
                                          to_address=mainWallet.address, amount= int(balance - gasWei), gas_limit=gas,
                                          gas_price=gas_price)
                print(wallet.address,txn.tran_hash.hex())
                time.sleep(2)
                # result = txn.wait()
                # print("账户%s, 余额: %s ETH , 转账: %s, 成功:%s , txnId=%s" % (
                #     wallet.address, client.to_human_num(balance), client.to_human_num(balance - gasWei), str(result['status'] == 1),
                #     result['transactionHash'].hex()))
            lastAddress = wallet.address
    except:
        traceback.print_exc()
        if lastAddress is not None:
            _saveProgress(command, lastAddress)


def query_wallets_balance():
    wallets, lastAddress, totalSize = readTaskAndProgress()
    for wallet in wallets:
        balance = client.get_balance(wallet.address)
        print("账户%s, 余额: %s %s." % (wallet.address, client.to_human_num(balance), client.symbol))


def query_wallets_erc20_token_balance():
    assert argv.erc20_contract is not None, "--erc20-contract 参数不能为空"
    wallets, lastAddress, totalSize = readTaskAndProgress()
    token = Erc20Token(argv.erc20_contract, web3=client.web3)
    for wallet in wallets:
        balance = token.balanceOfInHuman(wallet.address)
        print("账户%s, 余额: %s %s." % (wallet.address, balance, token.symbol))


# 给子账户转trx
if command == 'transfer_eth_to_wallets':
    transfer_eth_to_wallets()
# 归集指定的ERC20的token到主账户
if command == 'collect_erc20_token':
    collect_erc20_token()
# 归集ETH到主账户
if command == 'collect_eth':
    collect_eth()
# 查询子钱包的余额
if command == 'query_wallets_balance':
    query_wallets_balance()
# 查询子钱包的erc20 token的余额
if command == 'query_wallets_erc20_token_balance':
    query_wallets_erc20_token_balance()
