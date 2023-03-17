from const import UNIT_IN_BPS
from math import sqrt

GAS_USAGE = 350000


def arbitrage_action(
    x1: int, y1: int, x2: int, y2: int, r1_bps: int, r2_bps: int
) -> tuple[bool, str]:
    """
    Check if arbitrage condition is satisfied for 2 Uniswapv2 type DEXes

    Args:
        x1 (int): reserve of x token on the 1st DEX
        y1 (int): reserve of y token on the 1st DEX
        x2 (int): reserve of x token on the 2nd DEX
        y2 (int): reserve of y token on the 2nd DEX
        r1_bps (int): 1 - phi1 in basis points, where phi1 is the fee for 1st DEX
        r2_bps (int): 1 - phi2 in basis points, where phi2 is the fee for 2nd DEX

    Returns:
        bool: Returns True if arbitrage opportunity exists and False otherwise
    """

    if x2*y1*r1_bps*r2_bps > 100_000_000*x1*y2:
        return 'Sell Eth at Uni'

    if x1*y2*r1_bps*r2_bps > 100_000_000*x2*y1:
        return 'Sell Eth at Sushi'
    return '-'

def arbitrage_condition(
    x1: int, y1: int, x2: int, y2: int, r1_bps: int, r2_bps: int
) -> tuple[bool, str]:
    """
    Check if arbitrage condition is satisfied for 2 Uniswapv2 type DEXes

    Args:
        x1 (int): reserve of x token on the 1st DEX
        y1 (int): reserve of y token on the 1st DEX
        x2 (int): reserve of x token on the 2nd DEX
        y2 (int): reserve of y token on the 2nd DEX
        r1_bps (int): 1 - phi1 in basis points, where phi1 is the fee for 1st DEX
        r2_bps (int): 1 - phi2 in basis points, where phi2 is the fee for 2nd DEX

    Returns:
        bool: Returns True if arbitrage opportunity exists and False otherwise
    """

    if x2*y1*r1_bps*r2_bps > 100_000_000*x1*y2:
        return True

    if x1*y2*r1_bps*r2_bps > 100_000_000*x2*y1:
        return True
    return False


def get_optimal_dx(
    x1: int, y1: int, x2: int, y2: int, r1_bps: int, r2_bps: int, dec: int
) -> int:
    """
    Calculate optimal dx for executing the arbitrage opportunity

    Args:
        x1 (int): reserve of x token on the 1st DEX
        y1 (int): reserve of y token on the 1st DEX
        x2 (int): reserve of x token on the 2nd DEX
        y2 (int): reserve of y token on the 2nd DEX
        r1_bps (int): 1 - phi1 in basis points, where phi1 is the fee for 1st DEX
        r2_bps (int): 1 - phi2 in basis points, where phi2 is the fee for 2nd DEX
        dec (int): decimals of x token

    Returns:
        int: Arbitrage optimal dx for swapping dx -> dy -> dx'
    """

    num = 10_000*int(sqrt(x1*y1*x2*y2*r1_bps*r2_bps)) - 100_000_000*x1*y2
    den = (10_000*r1_bps*y2 + r1_bps*r2_bps*y1) * (10**dec)
    return num // den


def get_optimal_profit(
    x1: int, y1: int, x2: int, y2: int, r1_bps: int, r2_bps: int, dec1: int, dec2: int
) -> int:
    """
    Returns maximized profit from executing of the arbitrage opportunity

    Args:
        x1 (int): reserve of x token on the 1st DEX
        y1 (int): reserve of y token on the 1st DEX
        x2 (int): reserve of x token on the 2nd DEX
        y2 (int): reserve of y token on the 2nd DEX
        r1_bps (int): 1 - phi1 in basis points, where phi1 is the fee for 1st DEX
        r2_bps (int): 1 - phi2 in basis points, where phi2 is the fee for 2nd DEX
        dec1 (int): decimals of x token
        dec2 (int): decimals of y token

    Returns:
        int: Maximized profit from executing the arbitrage opportunity
    """
    def calc_profit(x1, y1, x2, y2, r1_bps, r2_bps, dec):
        dx = get_optimal_dx(x1, y1, x2, y2, r1_bps, r2_bps, dec)
        dy = y1 * r1_bps * dx // (10_000 * x1 + r1_bps * dx)
        dx_new = x2 * r2_bps * dy // (10_000 * y2 + r2_bps * dy)
        return dx_new - dx

    arb_cond = arbitrage_condition(x1, y1, x2, y2, r1_bps, r2_bps)
    instr = arbitrage_action(x1, y1, x2, y2, r1_bps, r2_bps)
    if not arb_cond:
        return 0

    if instr == 'Sell Eth at Uni':
        return calc_profit(x1, y1, x2, y2, r1_bps, r2_bps, dec1)

    if instr == 'Sell Eth at Sushi':
        return calc_profit(x2, y2, x1, y1, r2_bps, r1_bps, dec2)
