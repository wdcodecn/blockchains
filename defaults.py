#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/1 14:17
# @Author  : 0x00006913
# @Site    : 
# @File    : defaults.py

CONF_MAINNET = {
    "http": "https://mainnet.infura.io/v3/336c4be32fd04e93ae19babe7180ba08",
    "websocket": "wss://mainnet.infura.io/ws/v3/336c4be32fd04e93ae19babe7180ba08",
    "etherscan": "https://api.etherscan.io/api?apikey=3H4IK2TD5K9462ACN2EDM5E321KVGFX3IH",
    "symbol": "ETH"
}

CONF_KOVAN = {
    "http": "https://kovan.infura.io/v3/336c4be32fd04e93ae19babe7180ba08",
    "websocket": "wss://kovan.infura.io/ws/v3/336c4be32fd04e93ae19babe7180ba08",
    "etherscan": "https://api-kovan.etherscan.io/api?apikey=3H4IK2TD5K9462ACN2EDM5E321KVGFX3IH",
    "symbol": "ETH"
}

CONF_BSC = {
    "http": "https://bsc-dataseed.binance.org",
    "websocket": "wss://bsc-ws-node.nariox.org:443",
    "etherscan": "https://api-kovan.etherscan.io/api?apikey=3H4IK2TD5K9462ACN2EDM5E321KVGFX3IH",
    "symbol": "BNB"
}

CONF_BSC_TEST = {
    "http": "https://data-seed-prebsc-1-s1.binance.org:8545/",
    "websocket": "",
    "etherscan": "",
    "symbol": "BNB"
}

CONF_HECO = {
    "http": "https://http-mainnet-node.huobichain.com",
    "websocket": "wss://ws-mainnet-node.huobichain.com",
    "etherscan": "",
    "symbol": "HT"
}

ALL = {
    "mainnet": CONF_MAINNET,
    "kovan": CONF_KOVAN,
    "bsc": CONF_BSC,
    "bsc-test": CONF_BSC_TEST,
    "heco": CONF_HECO,
}


def conf_for_name(name: str) -> dict:
    return ALL.get(name, None)
