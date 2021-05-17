import time
import traceback
from configparser import ConfigParser
from datetime import datetime

import eth_utils
from decimal import Decimal
import defaults
import bsc_tokens
from bakeryswap.bakeryswap import BakerySwapV2Client
from eth_client import EthClient
from erc_20_token import Erc20Token

cfg = ConfigParser()
cfg.read("app.ini")
privateKey = cfg.get('main', 'privateKey')
address = cfg.get('main', 'address')

print("读取账户成功:", address)
ethClient = EthClient(network="bsc")

bakeryswap = BakerySwapV2Client(address=address, private_key=privateKey, provider=defaults.CONF_BSC.get("http"))

USDT = Erc20Token(contract_address=bsc_tokens.TOKEN_USDT, web3=ethClient.web3)
BUSD = Erc20Token(contract_address=bsc_tokens.TOKEN_BUSD, web3=ethClient.web3)
WBNB = Erc20Token(contract_address=bsc_tokens.TOKEN_WBNB, web3=ethClient.web3)

# 设置gas价格
bakeryswap.gasPrice = eth_utils.to_wei(10, "gwei")

vaiBalance = USDT.balanceOf(address)
vaiBalanceInHuman = USDT.inHumanNum(vaiBalance)
# 交易滑点
slippage = 0.005
# 目标价格
targetOut = 0.01168984


def swap(token_in: Erc20Token, amount_in, token_out: Erc20Token):
    # 交易的路径
    trade_path = [token_in.contract_address, bsc_tokens.TOKEN_WBNB, token_out.contract_address]
    amount_out = bakeryswap.get_amounts_out(amount_in, trade_path)[-1]
    print("卖出:", token_in.inHumanNum(amount_in), token_in.symbol, "       最小收入:", token_out.inHumanNum(amount_out),
          token_out.symbol)
    res = bakeryswap.swap_exact_tokens_for_tokens(int(amount_in), int(amount_out * slippage), trade_path, address, int(time.time() + 60))
    print(res)


if __name__ == "__main__":
    swap(BUSD, 5 * BUSD.precision, USDT)
