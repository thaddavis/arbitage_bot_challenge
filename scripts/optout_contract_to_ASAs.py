from helpers.utils import get_private_key_from_mnemonic
import config
import json
import base64
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError
from algosdk.v2client import algod
from algosdk.encoding import decode_address


algod_client = algod.AlgodClient(config.algod_token, config.algod_url)
sender_private_key = get_private_key_from_mnemonic(
    config.account_a_mnemonic)
ASA1_asset_id: int = config.ASA_1
ASA2_asset_id: int = config.ASA_2


def optout_contract_to_ASAs():
    print('ASA1_asset_id', ASA1_asset_id)
    print('ASA2_asset_id', ASA2_asset_id)

    app_address = logic.get_application_address(config.app_id)

    print('app_id', config.app_id)
    print('app_address', app_address)

    sender_address = account.address_from_private_key(
        sender_private_key)

    params = algod_client.suggested_params()
    params.flat_fee = True
    # "* 2" is how to pool fees for optin inner group txn
    params.fee = constants.MIN_TXN_FEE * 3

    sender = sender_address
    # receiver = app_address

    app_args = [
        "OptoutContractToASAs",
        ASA1_asset_id,
        decode_address(
            "GVPNGHFMZAFO3ZWXJKQ532T562RJOY7HMCY3PX7BVIVED5SMZXP5ECCWX4"),  # close ASA 1 remainder to this address
        ASA2_asset_id,
        decode_address(
            "GVPNGHFMZAFO3ZWXJKQ532T562RJOY7HMCY3PX7BVIVED5SMZXP5ECCWX4"),  # close ASA 2 remainder to this address
    ]
    unsigned_txn = transaction.ApplicationNoOpTxn(
        sender, params, config.app_id, app_args, foreign_assets=[ASA1_asset_id, ASA2_asset_id])

    gid = transaction.calculate_group_id([unsigned_txn])
    unsigned_txn.group = gid  # type: ignore

    signed_txn = unsigned_txn.sign(sender_private_key)

    tx_id = algod_client.send_transactions([signed_txn])

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))

        print("Successfully Opted-out Contract to ASA's")
        print("Result confirmed in round: {}".format(
            confirmed_txn['confirmed-round']))
    except Exception as err:
        print('ERROR', err)


if __name__ == "__main__":
    optout_contract_to_ASAs()
