from helpers.utils import get_private_key_from_mnemonic
import config
import json
from algosdk.encoding import decode_address
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.encoding import encode_address

from clients.algod import algod_client

sender_private_key = get_private_key_from_mnemonic(
    config.account_a_mnemonic)
ASA1_asset_id: int = config.ASA_1
ASA2_asset_id: int = config.ASA_2


def call_contract_testnet():
    print('')
    print('call_arbitrage_bot_contract')
    print('')
    app_info = algod_client.application_info(config.app_id)

    creator_address = app_info['params']['creator']
    sender_address = account.address_from_private_key(
        sender_private_key)

    app_address = logic.get_application_address(config.app_id)
    print('')
    print('creator_address', creator_address)
    print('sender_address', sender_address)
    print('sender_private_key', sender_private_key)
    print('app_id', config.app_id)
    print('app_address', app_address)
    print('')
    print('ASA1_asset_id', ASA1_asset_id)

    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE * 3

    receiver = app_address
    sender = sender_address
    ASA_1_amount_in = 1708974
    ASA_2_amount_out = 2

    # send ASA1 for 1st swap to contract
    unsigned_txn_A = transaction.AssetTransferTxn(
        sender,  # sender (str): address of the sender
        params,  # sp (SuggestedParams): suggested params from algod
        receiver,  # receiver (str): address of the receiver
        ASA_1_amount_in,  # amt (int): amount of asset base units to send
        ASA1_asset_id,  # index (int): index of the asset,
    )

    app_args = [
        "DoSwap",  # 0 function name "DoSwap"
        ASA1_asset_id,  # 1 ASA_1
        ASA2_asset_id,  # 2 ASA_2
        config.pool_1_app_id,  # 3 POOL_1 app id
        decode_address(config.pool_1_address),  # 4 POOL_1 address
        config.pool_2_app_id,  # 5 POOL_2 app id
        decode_address(config.pool_2_address),  # 6 POOL_2
        ASA_2_amount_out  # 7 amount of ASA_2 receive in exchange
    ]
    unsigned_txn_B = transaction.ApplicationNoOpTxn(
        sender, params, config.app_id, app_args, foreign_assets=[config.ASA_1, config.ASA_2], accounts=[config.pool_1_address], foreign_apps=[config.pool_1_app_id, config.app_id])

    gid = transaction.calculate_group_id([unsigned_txn_A, unsigned_txn_B])

    unsigned_txn_A.group = gid  # type: ignore
    unsigned_txn_B.group = gid  # type: ignore

    signed_txn_A = unsigned_txn_A.sign(sender_private_key)
    signed_txn_B = unsigned_txn_B.sign(sender_private_key)

    signed_group = [signed_txn_A, signed_txn_B]

    # submit transaction
    tx_id = algod_client.send_transactions(signed_group)

    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4)

        print("Transaction information: {}".format(
            json.dumps(confirmed_txn, indent=4)))

        print("Succesfully called the arbitrage bot")
    except Exception as err:
        print(err)


if __name__ == "__main__":
    call_contract_testnet()


# BEFORE...

# PQTU6KMR5TMGZAT3HA5UIUVLYK5HCO5DDL5J6GAWII4YRPUBUOBBCB6GGI -> 9999999991
# YJ6LDUQDRTC6TNGV7TQVOBGKM7HAQ2UR6M54CMF47TU4GBFZZXYZD5TG34 -> 2615869467

# AFTER EXPECTED...

# PQTU6KMR5TMGZAT3HA5UIUVLYK5HCO5DDL5J6GAWII4YRPUBUOBBCB6GGI -> 9999999988
# YJ6LDUQDRTC6TNGV7TQVOBGKM7HAQ2UR6M54CMF47TU4GBFZZXYZD5TG34 -> 2615869470
