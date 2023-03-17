# Arbitrage scanner
You need to write CLI application that finds arbitrage opportunities between 2 Uniswap-like DEXes 
([Uniswap](https://v2.info.uniswap.org/home) and [Sushiswap](https://www.sushi.com/)) either for specific block range 

```bash
# Usage example
# Find all arbitrage opportunities in [from-block, to-block] for pairs.csv
python3 ascanner_range.py \
    --from-block 16000000 \
    --to-block 16000100 \
    --pairs pairs.csv \
    --provider-uri http://localhost:8545
```
or for newly mined blocks:

```bash
# Usage example
# Find all arbitrage opportunities in stream mode
python3 ascanner_stream.py --pairs pairs.csv --provider-uri http://localhost:8545
```
In other words, `ascanner_stream.py` should work forever and check every N seconds whether new block was mined and find 
arbitrage opportunities for predefined number of pairs in newly mined blocks.

## Workflow

1. **Please, read [`notes.ipynb`](/notes.ipynb) before you start.**
2. Examine how the project is organized. Read the code carefully.
    * [`const`](/const/) folder contains global constants that are needed for the project. Please, specify all global variables in [`const/__init__.py`](/const/__init__.py) if the need arises
    * [`utils/arbitrage.py`](/utils/arbitrage.py) contains utils for all the arbitrage checking and calculations. It is the core file that you are going to work with.
    * [`utils/providers.py`](/utils/providers.py) is needed for batch requests functionality
    * [`utils/requests.py`](/utils/requests.py) contains functions for batch requests creation
3. Use batch requests for the project. Unfortunately, [https://getblock.io/](https://getblock.io/) doesn't provide archive nodes in their free plan, but it is still recommended to use it in [`notes.ipynb`](/notes.ipynb) for deriving the pivot table of pairs. For archive nodes one can use [https://www.infura.io/](https://www.infura.io/) or [https://www.alchemy.com/](https://www.alchemy.com/). Archive nodes provide the functionality for extracting any smart contract data as of any past block, while full nodes (as [https://getblock.io/](https://getblock.io/)) keep this kind of data for the last 128 blocks.
4. Note that python float precision may be inapplicable for the project. It is strongly recommended to work with floating point numbers via [decimal class](https://docs.python.org/3/library/decimal.html) to avoid precision errors.

Good luck!
