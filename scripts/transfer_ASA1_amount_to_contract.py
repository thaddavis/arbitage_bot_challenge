from helpers.utils import get_private_key_from_mnemonic
import config
import json
import base64
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from algosdk.v2client import algod
from algosdk.encoding import encode_address


algod_client = algod.AlgodClient(config.algod_token, config.algod_address)
sender_private_key = get_private_key_from_mnemonic(
    config.account_c_mnemonic)

ASA1_asset_id: int = config.ASA1


def transfer_ASA1_amount_to_contract():

    app_address = logic.get_application_address(config.app_id)
    print('')
    print('app address: ', app_address)
    print('')

    # print("app_info: {}".format(
    #     json.dumps(app_info, indent=4))
    # )

    asset_info = algod_client.asset_info(ASA1_asset_id)
    sender_address = account.address_from_private_key(
        sender_private_key)
    receiver_address = app_address

    print('')
    print('sender_address', sender_address)
    print('receiver_address', receiver_address)
    print('ASA creator', asset_info['params']['creator'])
    print('')

    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    sender = sender_address
    receiver = receiver_address

    unsigned_txn_A = transaction.AssetTransferTxn(
        sender,  # sender (str): address of the sender
        params,  # sp (SuggestedParams): suggested params from algod
        receiver,  # receiver (str): address of the receiver
        2,  # amt (int): amount of asset base units to send
        ASA1_asset_id  # index (int): index of the asset
    )

    print("signing opt-in txn")
    signed_txn_A = unsigned_txn_A.sign(sender_private_key)

    # submit transaction
    print("sending txn")
    tx_id = algod_client.send_transactions([signed_txn_A])

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4)

        print("Asset amount transferred successfully")
        print("Result confirmed in round: {}".format(
            confirmed_txn['confirmed-round']))
    except Exception as err:
        print('ERROR', err)


if __name__ == "__main__":
    transfer_ASA1_amount_to_account()
