# Arbitrage scanner
Our goal is to find arbitrage opportunities between 2 Uniswap-like DEXes 
([Uniswap](https://v2.info.uniswap.org/home) and [Sushiswap](https://www.sushi.com/)) for newly mined blocks:

```bash
# Usage example
# Find all arbitrage opportunities in stream mode
#Find existing pairs of tokens
python3 generate_pairs.py
#Find the arbitrage opportunities
python3 ascanner_stream.py
```

## Repo discription

* In [`notes.ipynb`](/notes.ipynb) basic info about project is presented

* [`const`](/const/) folder contains global constants that are needed for the project.
* [`utils/arbitrage.py`](/utils/arbitrage.py) contains utils for all the arbitrage checking and calculations.
* [`utils/providers.py`](/utils/providers.py) is needed for batch requests functionality
* [`utils/requests.py`](/utils/requests.py) contains functions for batch requests creation

## Important note

Python float precision may be inapplicable for the project. So, the work is done with floating point numbers via [decimal class](https://docs.python.org/3/library/decimal.html) to avoid precision errors.