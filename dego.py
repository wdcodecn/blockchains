#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/5 00:26
# @Author  : 0x00006913
# @Site    : 
# @File    : dego.py

import argparse
import json
from configparser import ConfigParser
from erc_20_token import Erc20Token
import os
import traceback
from wallet import Wallet
from eth_client import EthClient, TransactionRet
import eth_utils
from web3 import Web3

parser = argparse.ArgumentParser()
command = "dandy_airdrop"
ABI = json.loads(
    '[{"constant":false,"inputs":[{"name":"operator","type":"address"},{"name":"from","type":"address"},{"name":"tokenId","type":"uint256"},{"name":"data","type":"bytes"}],"name":"onERC721Received","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"degoAmount","type":"uint256"},{"name":"resId","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"_governance","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"value","type":"uint256"}],"name":"setMinMintAmount","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"b","type":"bool"}],"name":"setMintDandy","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"_currentClaimKryptonite","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"minter","type":"address"}],"name":"removeMinter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"_minters","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_isUserStart","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"tokenId","type":"uint256"}],"name":"burn","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"_gegoes","outputs":[{"name":"id","type":"uint256"},{"name":"grade","type":"uint256"},{"name":"quality","type":"uint256"},{"name":"degoAmount","type":"uint256"},{"name":"createdTime","type":"uint256"},{"name":"blockNum","type":"uint256"},{"name":"resId","type":"uint256"},{"name":"author","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_dandyMintAmount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"claim","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"value","type":"uint256"}],"name":"setDandyMintAmount","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"_gego","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_airdropDegoAmount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"tokenId","type":"uint256"}],"name":"getGego","outputs":[{"name":"grade","type":"uint256"},{"name":"quality","type":"uint256"},{"name":"degoAmount","type":"uint256"},{"name":"createdTime","type":"uint256"},{"name":"blockNum","type":"uint256"},{"name":"resId","type":"uint256"},{"name":"author","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_dego","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"degoAmount","type":"uint256"}],"name":"addAirdropDego","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"_gegoId","outputs":[{"name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"value","type":"uint256"}],"name":"setMaxClaimKryptonite","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"minter","type":"address"}],"name":"addMinter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"_stakeDegoForKryptonite","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_isClaimStart","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"start","type":"bool"}],"name":"setClaimStart","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"governance","type":"address"}],"name":"setGovernance","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"_minMintAmount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getQualityBase","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_canMintDandy","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"member","type":"address"}],"name":"removeTopMember","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"_claimMembers","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_maxClaimKryptonite","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"users","type":"address[]"},{"name":"openTag","type":"bool"}],"name":"setTopMember","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"_minBurnTime","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"_topMembers","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"start","type":"bool"}],"name":"setUserStart","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"_qualityBase","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"quality","type":"uint256"}],"name":"getGrade","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"gego","type":"address"}],"name":"setGegoContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"minBurnTime","type":"uint256"}],"name":"setMinBurnTime","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"member","type":"address"}],"name":"addTopMember","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"_dandy","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_maxGradeLong","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_maxGrade","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dego","type":"address"}],"name":"setDegoContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"dego","type":"address"},{"name":"gego","type":"address"},{"name":"dandy","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"id","type":"uint256"},{"indexed":false,"name":"grade","type":"uint256"},{"indexed":false,"name":"quality","type":"uint256"},{"indexed":false,"name":"degoAmount","type":"uint256"},{"indexed":false,"name":"createdTime","type":"uint256"},{"indexed":false,"name":"blockNum","type":"uint256"},{"indexed":false,"name":"resId","type":"uint256"},{"indexed":false,"name":"author","type":"address"}],"name":"GegoAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"id","type":"uint256"},{"indexed":false,"name":"degoAmount","type":"uint256"}],"name":"GegoBurn","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"operator","type":"address"},{"indexed":false,"name":"from","type":"address"},{"indexed":false,"name":"tokenId","type":"uint256"},{"indexed":false,"name":"data","type":"bytes"}],"name":"NFTReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"GovernanceTransferred","type":"event"}]')

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
    "--max-gas-price",
    type=int,
    help="指定最大的交易gas价格，会根据gas orcale匹配当前最划算的gas。 如果超出了则继续等待到合适的价格")

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
    "--contract",
    type=str,
    default="0x9765fea9752505a685c1bce137ae5b2efe8ddf62",
    help="空投的合约地址")

argv = parser.parse_args()
client = EthClient(network=argv.network)

CONTRACT_ADDRESS = Web3.toChecksumAddress(argv.contract)
contract = client.web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

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


def readWalletsFromFile(file):
    wallets = []
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            pair = line.replace("\n", "").split(" ")
            wallets.append(Wallet(Web3.toChecksumAddress(pair[1]), pair[0], eth_client=client))
    return wallets


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


def isClaim(address):
    return contract.caller()._claimMembers(address)


def claim(wallet: Wallet):
    txn = {
        'chainId': client.chain_id,
        'gas': argv.gas,
        'gasPrice': eth_utils.to_wei(argv.gas_price, "gwei"),
        'nonce': client.web3.eth.getTransactionCount(wallet.address),
        'from': wallet.address
    }
    transfer_txn = contract.functions.claim().buildTransaction(txn)
    signed_tran =  client.web3.eth.account.sign_transaction(transfer_txn, private_key=wallet.private_key)
    tran_hash = client.web3.eth.sendRawTransaction(signed_tran.rawTransaction)
    return TransactionRet(tran_hash=tran_hash, web3=client.web3)

wallets, lastAddress, totalSize = readTaskAndProgress()

try:
    print("开始领取%d个账户的空投, 剩余%d个账户" % (totalSize, len(wallets)))
    for wallet in wallets:
        if isClaim(wallet.address):
            print("钱包 %s 已经领取过空投" % wallet.address)
            continue
        ret = claim(wallet).wait()
        lastAddress = wallet.address
        print(wallet.address, ret['transactionHash'].hex())

except:
    traceback.print_exc()
    if lastAddress is not None:
        _saveProgress(command, lastAddress)

print("转账任务结束.....")
_clearProgress(command)

