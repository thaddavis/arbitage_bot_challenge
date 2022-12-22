from helpers.utils import get_private_key_from_mnemonic
import config
import json
import base64
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from algosdk.v2client import algod
from algosdk.encoding import encode_address

from clients.algod import algod_client

account_private_key = get_private_key_from_mnemonic(
    config.account_a_mnemonic)
ASA_asset_id: int = config.ASA_1


def optin_account_to_ASA():
    print('ASA_asset_id', ASA_asset_id)
    app_info = algod_client.application_info(config.app_id)

    creator_address = app_info['params']['creator']
    account_address = account.address_from_private_key(
        account_private_key)

    assert creator_address == account_address

    app_address = logic.get_application_address(config.app_id)
    print('app_address', app_address)

    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    sender = account_address

    unsigned_txn_A = transaction.AssetTransferTxn(
        sender,  # sender (str): address of the sender
        params,  # sp (SuggestedParams): suggested params from algod
        sender,  # receiver (str): address of the receiver
        0,  # amt (int): amount of asset base units to send
        ASA_asset_id  # index (int): index of the asset
    )

    print("signing opt-in txn")
    signed_txn_A = unsigned_txn_A.sign(account_private_key)

    # submit transaction
    print("sending txn")
    tx_id = algod_client.send_transactions([signed_txn_A])

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))

        print("Opted-in successfully")
        print("Result confirmed in round: {}".format(
            confirmed_txn['confirmed-round']))
    except Exception as err:
        print('ERROR', err)


if __name__ == "__main__":
    optin_account_to_ASA()
