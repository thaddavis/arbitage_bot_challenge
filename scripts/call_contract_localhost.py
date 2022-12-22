from helpers.utils import get_private_key_from_mnemonic
import config
import json
from algosdk.encoding import decode_address
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from algosdk.v2client import algod
from algosdk.encoding import encode_address


algod_client = algod.AlgodClient(
    config.algod_token, config.algod_url)
sender_private_key = get_private_key_from_mnemonic(
    config.account_a_mnemonic)
ASA1_asset_id: int = config.ASA_1
ASA2_asset_id: int = config.ASA_2


def call_contract_localhost():
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
    params.fee = constants.MIN_TXN_FEE * 2

    receiver = app_address
    sender = sender_address
    # send ASA1 for 1st swap to contract
    unsigned_txn_A = transaction.AssetTransferTxn(
        sender,  # sender (str): address of the sender
        params,  # sp (SuggestedParams): suggested params from algod
        receiver,  # receiver (str): address of the receiver
        3,  # amt (int): amount of asset base units to send
        ASA1_asset_id,  # index (int): index of the asset
    )

    app_args = [
        "DoSwap",  # function name "DoSwap"
        ASA1_asset_id,  # ASA_1
        "",  # ASA_2
        decode_address(config.pool_1_address),  # POOL_1
        decode_address(config.pool_2_address),  # POOL_2
        4  # amount of ASA_1 to send back to the sender
    ]
    unsigned_txn_B = transaction.ApplicationNoOpTxn(
        sender, params, config.app_id, app_args, foreign_assets=[config.ASA_1])

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

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))

        print("Succesfully called the arbitrage bot")
    except Exception as err:
        print(err)


if __name__ == "__main__":
    call_contract_localhost()
