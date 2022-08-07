from brownie import *
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import time

load_dotenv()

# environment variables
WALLET = os.getenv('WALLET')
MIN_REWARD = float(os.getenv('MIN_REWARD'))
MAX_GAS = float(os.getenv('MAX_GAS'))

# constants
LDO = '0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32'
stethCRVPOOL = '0xDC24316b9AE028F1497c275EB9192a3Ea0f67022'
stethCRVGAUGE = '0x182B723a58739a9c974cFDB385ceaDb237453c28'

# brownie init
network.connect('mainnet')
p = project.load()
pool = p.interface.pool(stethCRVPOOL)
gauge = p.interface.gauge(stethCRVGAUGE)

# here we calculate the amount of eth/steth that you would get if you'd withdraw
# all your curve pool tokens in eth or in steth
token_balance = gauge.balanceOf(WALLET)
all_eth = pool.calc_withdraw_one_coin(token_balance, 0)
all_steth = pool.calc_withdraw_one_coin(token_balance, 1)
ldo_pending = gauge.claimable_reward(WALLET, LDO)


# prices, all from chainlink
def get_price(oracle):
    decimals = oracle.decimals()
    price_raw = oracle.latestRoundData()[1]
    return price_raw / 10 ** decimals


cl_eth = p.interface.chainlink('0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419')
eth_price = get_price(cl_eth)
eth_value = round((all_eth / 1e18) * eth_price, 2)

cl_steth = p.interface.chainlink('0xCfE54B5cD566aB89272946F602D76Ea879CAb4a8')
steth_price = get_price(cl_steth)
steth_value = round((all_steth / 1e18) * steth_price, 2)

cl_ldo = p.interface.chainlink('0x4e844125952D32AcdF339BE976c98E22F6F318dB')
ldo_price = get_price(cl_ldo) * eth_price
ldo_value = round((ldo_pending / 1e18) * ldo_price, 2)

# here we use the eth value converted to dollar amounts and add pending ldo dollar amounts
net_value = round(eth_value + ldo_value, 2)

# creating dictionary
now = int(round(time.time()))

di = {'date': str(datetime.fromtimestamp(now)),
      'timestamp': now,
      'pool_tokens': round(token_balance / 1e18, 2),
      'eth_tokens': round(all_eth / 1e18, 2),
      'eth_value': eth_value,
      'steth_tokens': round(all_steth / 1e18, 2),
      'steth_value': steth_value,
      'ldo_tokens': round(ldo_pending / 1e18, 2),
      'ldo_value': ldo_value,
      'net_value': net_value}

# reading old data into dataframe, adding new data
if os.path.exists('data.csv'):
    df1 = pd.read_csv('data.csv', index_col=False)
    df2 = pd.DataFrame([di])
    df3 = pd.concat([df1, df2])
    df3.to_csv('data.csv', index=False)
else:
    df1 = pd.DataFrame([di])
    df1.to_csv('data.csv', index=False)

# additionally claim LDO token rewards if conditions are met
if ldo_value > MIN_REWARD and (chain.base_fee / 1e9 < MAX_GAS):
    key = os.getenv('WORKER')
    account = accounts.add(key)
    gauge.claim_rewards(WALLET, {'from': account})
