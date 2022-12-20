import json
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
import config
from helpers.utils import get_private_key_from_mnemonic

algod_client = algod.AlgodClient(config.algod_token, config.algod_address)


def get_assets_info_of_account():
    account = config.account_a
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    account_info = algod_client.account_info(account)

    print("Account Information: {}".format(
        json.dumps(account_info, indent=4)))


if __name__ == "__main__":
    get_assets_info_of_account()
