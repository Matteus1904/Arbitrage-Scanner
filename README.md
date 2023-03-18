# Arbitrage scanner
Our goal is to find arbitrage opportunities between 2 Uniswap-like DEXes 
([Uniswap](https://v2.info.uniswap.org/home) and [Sushiswap](https://www.sushi.com/)) either for specific block range 

```bash
# Usage example
# Find all arbitrage opportunities in stream mode
python3 ascanner_stream.py
```
In other words, `ascanner_stream.py` should work forever and check every N seconds whether new block was mined and find 
arbitrage opportunities for predefined number of pairs in newly mined blocks.

## Repo discription

* In [`notes.ipynb`](/notes.ipynb) basic info about project is presented

* [`const`](/const/) folder contains global constants that are needed for the project.
* [`utils/arbitrage.py`](/utils/arbitrage.py) contains utils for all the arbitrage checking and calculations.
* [`utils/providers.py`](/utils/providers.py) is needed for batch requests functionality
* [`utils/requests.py`](/utils/requests.py) contains functions for batch requests creation

## Important note

Python float precision may be inapplicable for the project. So, the work is done with floating point numbers via [decimal class](https://docs.python.org/3/library/decimal.html) to avoid precision errors.