from web3 import Web3
import json
from const import ADDRESSES, UNISWAPV2_FACTORY_ABI, ERC20_ABI, UNISWAPV2_PAIR_ABI
import time
import os
from web3.middleware import geth_poa_middleware
from utils.providers import get_provider_from_uri
import pandas as pd

# Let us create py-web3 objects for Ethereum node DDOS
PROVIDER_URI = "https://eth.getblock.io/ee60e639-1307-4c20-8d64-f4441ea4b678/mainnet/"
BATCH_W3 = get_provider_from_uri(PROVIDER_URI, batch=True)
W3 = Web3(BATCH_W3)

UNISWAPV2_FACTORY_CONTRACT = W3.eth.contract(
    address=ADDRESSES.uniswapv2_factory, abi=UNISWAPV2_FACTORY_ABI
)

SUSHISWAPV2_FACTORY_CONTRACT = W3.eth.contract(
    address=ADDRESSES.sushiswapv2_factory, abi=UNISWAPV2_FACTORY_ABI
)

sender_address = input(f"Enter your address with WETH")

what_to_buy = pd.read_csv('what_to_buy.csv')

pr_key = input(f"Enter Private Key")

for i in range(what_to_buy.shape[0]):
    if what_to_buy.arb_act[i] == 'Sell Eth at Sushi':



        tokenToBuy = what_to_buy.token[i]   #Goal token
        spend = W3.toChecksumAddress("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")  # wrapped ether

        nonce = W3.eth.get_transaction_count(sender_address)

        sushiswapv2_txn = SUSHISWAPV2_FACTORY_CONTRACT.functions.swapExactETHForTokens(
            10000000000,
            [spend, tokenToBuy],
            sender_address,
            (int(time.time()) + 100000)
        ).buildTransaction({
            'from': sender_address,
            'value': W3.toWei(0.1, 'ether'),  
            'gas': 350000,
            'nonce': nonce,
        })

        signed_txn = W3.eth.account.sign_transaction(sushiswapv2_txn, private_key=pr_key)
        tx_token = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(W3.toHex(tx_token))

        tokenToBuy = W3.toChecksumAddress("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")  # wrapped ether
        spend = what_to_buy.token[i]  # wrapped ether

        nonce = W3.eth.get_transaction_count(sender_address)

        uniswapv2_txn = UNISWAPV2_FACTORY_CONTRACT.functions.swapExactETHForTokens(
            10000000000,
            [spend, tokenToBuy],
            sender_address,
            (int(time.time()) + 100000)
        ).buildTransaction({
            'from': sender_address,
            'value': W3.toWei(0.1, 'ether'),  
            'gas': 2000000,
            'nonce': nonce,
        })

        signed_txn = W3.eth.account.sign_transaction(uniswapv2_txn, private_key=pr_key)
        tx_token = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(W3.toHex(tx_token))

    else:
        tokenToBuy = what_to_buy.token[i]   #Goal token
        spend = W3.toChecksumAddress("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")  # wrapped ether

        nonce = W3.eth.get_transaction_count(sender_address)

        uniswapv2_txn = UNISWAPV2_FACTORY_CONTRACT.functions.swapExactETHForTokens(
            10000000000,
            [spend, tokenToBuy],
            sender_address,
            (int(time.time()) + 100000)
        ).buildTransaction({
            'from': sender_address,
            'value': W3.toWei(0.1, 'ether'),  
            'gas': 2000000,
            'nonce': nonce,
        })

        signed_txn = W3.eth.account.sign_transaction(uniswapv2_txn, private_key=pr_key)
        tx_token = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(W3.toHex(tx_token))

        tokenToBuy = W3.toChecksumAddress("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")  # wrapped ether
        spend = what_to_buy.token[i]  # wrapped ether

        nonce = W3.eth.get_transaction_count(sender_address)

        sushiswapv2_txn = SUSHISWAPV2_FACTORY_CONTRACT.functions.swapExactETHForTokens(
            10000000000,
            [spend, tokenToBuy],
            sender_address,
            (int(time.time()) + 100000)
        ).buildTransaction({
            'from': sender_address,
            'value': W3.toWei(0.1, 'ether'),  
            'gas': 350000,
            'nonce': nonce,
        })

        signed_txn = W3.eth.account.sign_transaction(sushiswapv2_txn, private_key=pr_key)
        tx_token = W3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(W3.toHex(tx_token))