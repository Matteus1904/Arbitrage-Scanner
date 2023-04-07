# Arbitrage scanner
Arbitrage is the simultaneous purchase and sale of the same or similar asset in different markets in order to profit from tiny differences in the asset's listed price. In our project we theoretically derive an amount of tokens to be bought and sold in case of arbitrage opportunity between two Uniswap-like DEXes ([Uniswap](https://v2.info.uniswap.org/home) and [Sushiswap](https://www.sushi.com/)) for newly mined blocks. We implement the scanner as a batch request system using Web3 framework and a separate module to execute transactions. During testing at specific points of time, our implementation shows its ability to find arbitrage opportunities and calculate the profits, and demonstrates its time efficiency.

```bash
# Usage example
# Find all arbitrage opportunities in stream mode
#Find existing pairs of tokens
python3 generate_pairs.py
#Find the arbitrage opportunities
python3 ascanner_stream.py
```

## Repo description

* In [`notes.ipynb`](/notes.ipynb) basic info about project is presented

* In [`generate_pairs.py`](/generate_pairs.py) existing pairs between uniswap and sushiswap are collected (more info can be found in [`notes.ipynb`](/notes.ipynb)). The approximate time of execution is 10 minutes, what is bad for high-frequency arbitrage trading, but the point is that there is no need in constant execution of this script: arbitrage can be found in old pairs as well. So, the pairs can be updated once a day, for example.

* [`pairs.csv`](/pairs.csv) is the resulting file of above script and contains fields with info about addreses of correspoding pairs of sushiswap and uniswap

* In [`ascanner_stream.py`](/ascanner_stream.py) the potential arbitrage profits and chooses the pairs, where arbitrage exist, the resulting file is [`what_to_buy.csv`](/what_to_buy.csv) which have such field as `Name` - the name of token with arbitrage opportunity, `Token` - address of the token, `Arb_cond` - should be True everywhere - to make true that arbitrage exist, `Arb_act` -  the direction, at which the arbitrage should be performed, `Profit_USD` and `ROE_in_%` - fields indicating the power of arbitrage

* [`calculate_all.csv`](/calculate_all.csv) - technical file with the same structure, as what_to_buy.csv, but contains all calculated pairs - needed for gathering statistics 

* [`stats.csv`](/stats.csv) - file with statistics - number of arbitrage opportuninies, sum of potential arb profits in USD, and ROE at specific point of time

* In [`transaction_module.py`](/transaction_module.py) - run the transactions from what_to_buy file. Private key is needed. Aware that this operation can be risky - this module is not tested carefully yet due to the problems of running testnet in Uniswap and Sushiswap

* [`const`](/const/) folder contains global constants that are needed for the project.
* [`utils/arbitrage.py`](/utils/arbitrage.py) contains utils for all the arbitrage checking and calculations.
* [`utils/providers.py`](/utils/providers.py) is needed for batch requests functionality
* [`utils/requests.py`](/utils/requests.py) contains functions for batch requests creation

## Important note

Python float precision may be inapplicable for the project. So, the work is done with floating point numbers via [decimal class](https://docs.python.org/3/library/decimal.html) to avoid precision errors.
