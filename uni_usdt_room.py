import time
import traceback
from datetime import datetime

import eth_utils

import defaults
import eth_tokens
from uniswap.uniswap import UniswapV2Client
from eth_client import EthClient
from erc_20_token import Erc20Token
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read("app.ini")
privateKey = cfg.get('main', 'privateKey')
address = cfg.get('main', 'address')

print("读取账户成功:", address)
ethClient = EthClient(network="mainnet")

uniSwap = UniswapV2Client(address=address, private_key=privateKey, provider=defaults.CONF_MAINNET.get("http"))

ROOM = Erc20Token(contract_address=eth_tokens.TOKEN_ROOM, web3=ethClient.web3)
USDT = Erc20Token(contract_address=eth_tokens.TOKEN_USDT, web3=ethClient.web3)
WETH = Erc20Token(contract_address=eth_tokens.TOKEN_WETH, web3=ethClient.web3)

# 设置gas价格
uniSwap.gasPrice = eth_utils.to_wei(50, "gwei")

IN_TOKEN = USDT
OUT_TOKEN = ROOM

# 买入总额 500刀
IN_AMOUNT = 500
# 交易滑点 0.5% , 增加成功率的话可以调高一点
slippage = 0.05
# 目标单价格 ，10刀
targetOutUnit = 10

balance = IN_AMOUNT * IN_TOKEN.precision
balanceInHuman = IN_TOKEN.inHumanNum(balance)

# 交易的路径
trade_path = [IN_TOKEN.contract_address, eth_tokens.TOKEN_WETH, OUT_TOKEN.contract_address]

while True:
    try:
        out = uniSwap.get_amounts_out(balance, trade_path)
        amount_out = out[-1]
        vai_out = OUT_TOKEN.inHumanNum(amount_out)
        out_unit = balanceInHuman / vai_out
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "|", balanceInHuman, "=>", vai_out, "|", out_unit,
              IN_TOKEN.symbol, "per", OUT_TOKEN.symbol)

        if out_unit <= targetOutUnit:
            try:
                # if IN_TOKEN.balanceOfInHuman(address) < balanceInHuman:
                #     break
                # res = uniSwap.swap_exact_tokens_for_tokens(int(balance), int(amount_out * slippage), trade_path,
                #                                                address, int(time.time() + 60))
                # print(res)
                pass
            except:
                traceback.print_exc()
                time.sleep(60)
            time.sleep(3)
            # balance = IN_TOKEN.balanceOf(address)
            # balanceInHuman = IN_TOKEN.inHumanNum(balance)
        time.sleep(5)
    except KeyboardInterrupt:
        break
    except:
        traceback.print_exc()
