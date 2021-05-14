## 波场工具集合

### 初始化
- python版本 3.0+
- 安装依赖环境
```
pip install -r requirements.txt
```
- 配置app.ini
```
[main]
#主账户的私钥
privateKey=
#主账户的eth地址
address=
```
### 使用
- pancake 挂单脚本
> eg. 用USDT 买 KEY (需要自己编辑里面的金额，滑点参数等)
```
 python pancake_usdt_key.py 
```
- 批量给羊毛账户转指定的eth
> eg. 用主账户给wallet.txt中的账户转1个eth
```
   python app.py  transfer_eth_to_accounts --wallet-file wallet.txt --eth-amount 0.01 --gas 25000 --gas-price 50
```
- 归集任意ERC20资产到主账户
> eg. 归集 DANDY 代币到主账号. 0x9dfc4b433d359024eb3e810d77d60fbe8b0d9b82 是DANDY的代币合约地址
```
  python app.py collect_erc20_token  --wallet-file wallet.txt --erc20-contract --erc20-contract 0x9dfc4b433d359024eb3e810d77d60fbe8b0d9b82 --gas 25000 --gas-price 80
```
- 查询所有子钱包的ETH余额
```
python app.py query_wallets_balance --wallet-file wallect.txt
```

- 查询所有子钱包指定的ERC20 TOKEN的余额
> eg. 查询钱包的 DANDY 代币余额， 0x9dfc4b433d359024eb3e810d77d60fbe8b0d9b82 是DANDY代币的合约地址
```
python app.py query_wallets_erc20_token_balance --wallet-file wallet.txt --erc20-contract 0x9dfc4b433d359024eb3e810d77d60fbe8b0d9b82 
``` 

- 归集eth到主账户
> eg. 归集wallet.txt中的账户的eth到主账户
```
python app.py collect_eth --wallet-file wallet.txt --gas 21000 --gas-price 90
```
- dego 羊毛
> 测试网络中的dego空投
```
python dego.py --wallet-file wallet.txt --gas 646912 --gas-price 30 --network bsc-test --contract 0xca16d4af9f1d98e481ca43d8b0a3727de560fe5c

```

### 赞助

> 接受任意资产的赞助. 
- 波场钱包: TMKnSJLcxuxsraH9iKbdKFkrGKbvttQGRM
- 以太钱包: 0x72CDD10220E133fDa6c496d8a62A835046595b3C
- BTC钱包:  3CtEwBn2yM4bQ44puWSAxXm1ng69DQY7Vw
