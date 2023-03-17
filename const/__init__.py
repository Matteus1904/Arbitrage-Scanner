import json
import pathlib
from omegaconf import OmegaConf

PROJECT_DIR = pathlib.Path(__file__).parent.parent.resolve()
JSON_ABIS_DIR = PROJECT_DIR / "const" / "json_abis"

with open(JSON_ABIS_DIR / "uniswapv2_factory.json", "r") as f:
    UNISWAPV2_FACTORY_ABI = json.load(f)

with open(JSON_ABIS_DIR / "uniswapv2_pair.json", "r") as f:
    UNISWAPV2_PAIR_ABI = json.load(f)

with open(JSON_ABIS_DIR / "erc20.json", "r") as f:
    ERC20_ABI = json.load(f)

UNIT_IN_BPS = 10000
DEFAULT_TIMEOUT = 60
ALL_PAIRS_CALL_HEX = (
    0x1E3DD18B0000000000000000000000000000000000000000000000000000000000000000
)
BALANCEOF_METHOD_ENCODED = "0x70a08231000000000000000000000000"
GET_RESERVES_METHOD_ENCODED = "0x0902f1ac"
TOKEN1_METHOD_ENCODED = "0xd21220a7"
TOKEN0_METHOD_ENCODED = "0x0dfe1681"


ADDRESSES = OmegaConf.load(PROJECT_DIR / "const" / "addresses.yaml")
