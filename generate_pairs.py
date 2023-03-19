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

# Let us create py-web3 objects for Ethereum node DDOS
PROVIDER_URI = "https://eth.getblock.io/ee60e639-1307-4c20-8d64-f4441ea4b678/mainnet/"
BATCH_W3 = get_provider_from_uri(PROVIDER_URI, batch=True)
W3 = Web3(BATCH_W3)


# Now let us extract pair addresses for the first 100 pairs via 1 batch request
UNISWAPV2_FACTORY_CONTRACT = W3.eth.contract(
    address=ADDRESSES.uniswapv2_factory, abi=UNISWAPV2_FACTORY_ABI
)
n_pairs = UNISWAPV2_FACTORY_CONTRACT.functions.allPairsLength().call()
print("TOTAL NUMBER OF PAIRS", n_pairs)

tokens0 = []
tokens1 = []
pair_addresses = []
balances = []
block_number = W3.eth.block_number
x = 23500
factory_address = ADDRESSES.uniswapv2_factory
for i in range(0, n_pairs//x + 1):
    pair_ids = range(i*x, min(x*(i+1), n_pairs))
    batch_request = json.dumps(
        [
            get_request_all_pairs(
                factory_address, pair_id, block_number, request_id=pair_id
            )
            for pair_id in pair_ids
        ]

    )

    batch_response = BATCH_W3.make_batch_request(batch_request)

    pair_address = [
        "0x" + response_item["result"][-40:]
        for response_item in batch_response
    ]

    # Extracting token0, token1

    token0_request = json.dumps(
        [
            get_request_token0(pair_address, block_number, request_id=i)
            for i, pair_address in enumerate(pair_address)
        ]
    )

    batch_response = BATCH_W3.make_batch_request(token0_request)
    tokens0 += [
        "0x" + response_item["result"][-40:]
        for response_item in batch_response
    ]

    token1_request = json.dumps(
        [
            get_request_token1(pair_address, block_number, request_id=i)
            for i, pair_address in enumerate(pair_address)
        ]
    )
    batch_response = BATCH_W3.make_batch_request(token1_request)
    tokens1 += [
        "0x" + response_item["result"][-40:]
        for response_item in batch_response
    ]

    # Well, let us calculate how many WETH tokens are located in each pair

    liquidity_request = json.dumps(
        [
            get_request_balanceof(ADDRESSES.weth, pair_address, block_number, request_id=i)
            for i, pair_address in enumerate(pair_address)
        ]
    )
    batch_response = BATCH_W3.make_batch_request(liquidity_request)
    balances += [
        hex_to_dec(response_item["result"])
        for response_item in batch_response
    ]

    pair_addresses += pair_address

uniswap = pd.DataFrame(
{
    "pair_address": pair_addresses,
    "token0": tokens0,
    "token1": tokens1,
    "WETH_balance": balances,
}
)


# Now let us extract pair addresses for the first 100 pairs via 1 batch request
UNISWAPV2_FACTORY_CONTRACT = W3.eth.contract(
    address=ADDRESSES.sushiswapv2_factory, abi=UNISWAPV2_FACTORY_ABI
)
n_pairs = UNISWAPV2_FACTORY_CONTRACT.functions.allPairsLength().call()
print("TOTAL NUMBER OF PAIRS", n_pairs)

tokens0 = []
tokens1 = []
pair_addresses = []
balances = []
block_number = W3.eth.block_number
x = 23500
factory_address = ADDRESSES.sushiswapv2_factory
for i in range(0, n_pairs//x + 1):
    pair_ids = range(i*x, min(x*(i+1), n_pairs))
    batch_request = json.dumps(
        [
            get_request_all_pairs(
                factory_address, pair_id, block_number, request_id=pair_id
            )
            for pair_id in pair_ids
        ]

    )

    batch_response = BATCH_W3.make_batch_request(batch_request)

    pair_address = [
        "0x" + response_item["result"][-40:]
        for response_item in batch_response
    ]

    # Extracting token0, token1

    token0_request = json.dumps(
        [
            get_request_token0(pair_address, block_number, request_id=i)
            for i, pair_address in enumerate(pair_address)
        ]
    )

    batch_response = BATCH_W3.make_batch_request(token0_request)
    tokens0 += [
        "0x" + response_item["result"][-40:]
        for response_item in batch_response
    ]

    token1_request = json.dumps(
        [
            get_request_token1(pair_address, block_number, request_id=i)
            for i, pair_address in enumerate(pair_address)
        ]
    )
    batch_response = BATCH_W3.make_batch_request(token1_request)
    tokens1 += [
        "0x" + response_item["result"][-40:]
        for response_item in batch_response
    ]

    # Well, let us calculate how many WETH tokens are located in each pair

    liquidity_request = json.dumps(
        [
            get_request_balanceof(ADDRESSES.weth, pair_address, block_number, request_id=i)
            for i, pair_address in enumerate(pair_address)
        ]
    )
    batch_response = BATCH_W3.make_batch_request(liquidity_request)
    balances += [
        hex_to_dec(response_item["result"])
        for response_item in batch_response
    ]

    pair_addresses += pair_address

sushiswap = pd.DataFrame(
{
    "pair_address": pair_addresses,
    "token0": tokens0,
    "token1": tokens1,
    "WETH_balance": balances,
}
)


sushi = sushiswap[((sushiswap.token0 == ADDRESSES.weth.lower()) | (sushiswap.token1 == ADDRESSES.weth.lower())) & (sushiswap.WETH_balance >= 10**18)]
uni = uniswap[((uniswap.token0 == ADDRESSES.weth.lower()) | (uniswap.token1 == ADDRESSES.weth.lower())) & (uniswap.WETH_balance >= 10**18)]


pairs = pd.merge(uni, sushi, on=['token0', 'token1'], how = 'inner', suffixes = ['_uni', '_sushi'])


import numpy as np
pairs['token'] = np.where(pairs.token0 == ADDRESSES.weth.lower(), pairs.token1,
                   np.where(pairs.token1 == ADDRESSES.weth.lower(), pairs.token0, np.nan))

pairs = pairs[['token0', 'token1', 'token', 'pair_address_sushi', 'pair_address_uni']]


pairs.to_csv('pairs.csv')