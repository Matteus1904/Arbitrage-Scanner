# import argparse
# from utils.providers import get_provider_from_uri

# parser = argparse.ArgumentParser(
#     prog="Arbitrage Scanner stream mode",
#     description="The project enables users find arbitrage opportunities in evm blockchains in stream mode",
# )


# parser.add_argument("--pairs", type=str, default=None, required=True)
# parser.add_argument("--provider-uri", type=str, default=None, required=True)

# args = parser.parse_args()

# batch_w3 = get_provider_from_uri(args.provider_uri, batch=True)

# # <YOUR CODE GOES HERE>
# # You can use any libraries you want
to_gwei = 1_000_000_000

from utils.providers import get_provider_from_uri
from utils import hex_to_dec
from utils.requests import (
    get_request_all_pairs,
    get_request_balanceof,
    get_request_token0,
    get_request_token1,
    get_request_get_reserves,
)
import json
from const import ADDRESSES, UNISWAPV2_FACTORY_ABI, ERC20_ABI, UNISWAPV2_PAIR_ABI
import pandas as pd
from web3 import Web3
import numpy as np

pd.options.mode.chained_assignment = None

final = pd.read_csv('final.csv') 

# Let us create py-web3 objects for Ethereum node DDOS
PROVIDER_URI = "https://eth.getblock.io/ee60e639-1307-4c20-8d64-f4441ea4b678/mainnet/"
BATCH_W3 = get_provider_from_uri(PROVIDER_URI, batch=True)
W3 = Web3(BATCH_W3)

block_number = W3.eth.block_number

get_reserves_request = json.dumps(
    [
        get_request_get_reserves(pair_address, block_number, request_id=i)
        for i, pair_address in enumerate(final.pair_address_uni)
    ]
)
batch_response = BATCH_W3.make_batch_request(get_reserves_request)

batch_response
reserves_uni = balances = [
    (hex_to_dec(response_item["result"][:66]), hex_to_dec(response_item["result"][66:130]))
    for response_item in batch_response
]

get_reserves_request = json.dumps(
    [
        get_request_get_reserves(pair_address, block_number, request_id=i)
        for i, pair_address in enumerate(final.pair_address_sushi)
    ]
)
batch_response = BATCH_W3.make_batch_request(get_reserves_request)

batch_response
reserves_sushi = balances = [
    (hex_to_dec(response_item["result"][:66]), hex_to_dec(response_item["result"][66:130]))
    for response_item in batch_response
]


res0_uni, res1_uni = zip(*reserves_uni)
res0_sushi, res1_sushi = zip(*reserves_sushi)

final['res0_uni'] = res0_uni
final['res1_uni'] = res1_uni

final['res0_sushi'] = res0_sushi
final['res1_sushi'] = res1_sushi

final['other_balance_uni'] = np.where(final.token0 == ADDRESSES.weth.lower(), final.res1_uni,
                   np.where(final.token1 == ADDRESSES.weth.lower(), final.res0_uni, np.nan))

final['other_balance_sushi'] = np.where(final.token0 == ADDRESSES.weth.lower(), final.res1_sushi,
                   np.where(final.token1 == ADDRESSES.weth.lower(), final.res0_sushi, np.nan))


def get_param_get_reserves(address):
    return {"to": address, "data": '0x313ce567'}


def generate_json_rpc(method, params, request_id=1):
    return {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id,
    }



def get_request_get_decimals(token, block_identifier, request_id):
    return generate_json_rpc(
        method="eth_call",
        params=[
            get_param_get_reserves(token),
            hex(block_identifier),
        ],
        request_id=request_id,
    )

get_reserves_decimals = json.dumps(
    [
        get_request_get_decimals(token, block_number, request_id=i)
        for i, token in enumerate(final.token)
    ]
)
batch_response = BATCH_W3.make_batch_request(get_reserves_decimals)

batch_response
decimals = [
    int(response_item["result"], 16)
    for response_item in batch_response
]

final['decimals'] = decimals

calculate_all = final[['WETH_balance_uni', 'WETH_balance_sushi', 'decimals' , 'other_balance_uni', 'other_balance_sushi', 'token']]

from utils import arbitrage

calculate_all['arb_cond'] = calculate_all.apply(
    lambda x: arbitrage.arbitrage_condition(
        x1=int(x['WETH_balance_uni']),
        y1=int(x['other_balance_uni']),
        x2=int(x['WETH_balance_sushi']),
        y2=int(x['other_balance_sushi']),
        r1_bps=9970,
        r2_bps=9970
    ),
    axis=1
)

calculate_all['arb_act'] = calculate_all.apply(
    lambda x: arbitrage.arbitrage_action(
        x1=int(x['WETH_balance_uni']),
        y1=int(x['other_balance_uni']),
        x2=int(x['WETH_balance_sushi']),
        y2=int(x['other_balance_sushi']),
        r1_bps=9970,
        r2_bps=9970
    ),
    axis=1
)

calculate_all['optimal_dx'] = calculate_all.apply(
    lambda x: arbitrage.get_optimal_dx(
        x1=int(x['WETH_balance_uni']),
        y1=int(x['other_balance_uni']),
        x2=int(x['WETH_balance_sushi']),
        y2=int(x['other_balance_sushi']),
        r1_bps=9970,
        r2_bps=9970,
        dec = int(x['decimals'])
    ),
    axis=1
)

calculate_all['profit_USD'] = calculate_all.apply(
    lambda x: arbitrage.get_optimal_profit(
        x1=int(x['WETH_balance_uni']),
        y1=int(x['other_balance_uni']),
        x2=int(x['WETH_balance_sushi']),
        y2=int(x['other_balance_sushi']),
        r1_bps=9970,
        r2_bps=9970,
        dec1 = 18,
        dec2 = int(x['decimals'])
    ),
    axis=1
)

calculate_all['optimal_dx'] = calculate_all['optimal_dx']/to_gwei

calculate_all['ROE_in_%'] = (100*calculate_all['profit_USD'])/(abs(1820*calculate_all['optimal_dx']))


what_to_buy = calculate_all[(calculate_all['arb_cond'])&(calculate_all['profit_USD']>0)]
what_to_buy = what_to_buy[['token','arb_cond', 'arb_act', 'profit_USD', 'ROE_in_%']]


name= []
for i in list(what_to_buy.token):
    token_contract = W3.eth.contract(address=Web3.toChecksumAddress(i), abi=ERC20_ABI)
    name  += [token_contract.functions.name().call()]

what_to_buy['name'] = name
what_to_buy = what_to_buy[['name', 'token','arb_cond', 'arb_act', 'profit_USD', 'ROE_in_%']]
what_to_buy.to_csv('what_to_buy.csv', index=False)
calculate_all.to_csv('calculate_all.csv', index = False)
