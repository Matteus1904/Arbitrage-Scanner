from const import (
    ALL_PAIRS_CALL_HEX,
    GET_RESERVES_METHOD_ENCODED,
    BALANCEOF_METHOD_ENCODED,
    TOKEN0_METHOD_ENCODED,
    TOKEN1_METHOD_ENCODED,
)


def generate_json_rpc(method, params, request_id=1):
    return {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id,
    }


def get_param_all_pairs(factory_address, pair_id):
    return {"to": factory_address, "data": hex(ALL_PAIRS_CALL_HEX + pair_id)}


def get_request_all_pairs(factory_address, pair_id, block_identifier, request_id):
    return generate_json_rpc(
        method="eth_call",
        params=[get_param_all_pairs(factory_address, pair_id), hex(block_identifier)],
        request_id=request_id,
    )


def get_param_balanceof(token_address, balanceof_address):
    param = {
        "to": token_address,
        "data": BALANCEOF_METHOD_ENCODED + balanceof_address[2:],
    }
    return param


def get_request_balanceof(token_address, wallet_address, block_identifier, request_id):
    return generate_json_rpc(
        method="eth_call",
        params=[
            get_param_balanceof(token_address, wallet_address),
            hex(block_identifier),
        ],
        request_id=request_id,
    )


def get_param_get_reserves(address):
    return {"to": address, "data": GET_RESERVES_METHOD_ENCODED}


def get_request_get_reserves(pair_address, block_identifier, request_id):
    return generate_json_rpc(
        method="eth_call",
        params=[
            get_param_get_reserves(pair_address),
            hex(block_identifier),
        ],
        request_id=request_id,
    )


def get_param_token0(pair_address):
    return {"to": pair_address, "data": TOKEN0_METHOD_ENCODED}


def get_param_token1(pair_address):
    return {"to": pair_address, "data": TOKEN1_METHOD_ENCODED}


def get_request_token0(pair_address, block_identifier, request_id):
    return generate_json_rpc(
        method="eth_call",
        params=[
            get_param_token0(pair_address),
            hex(block_identifier),
        ],
        request_id=request_id,
    )


def get_request_token1(pair_address, block_identifier, request_id):
    return generate_json_rpc(
        method="eth_call",
        params=[
            get_param_token1(pair_address),
            hex(block_identifier),
        ],
        request_id=request_id,
    )
