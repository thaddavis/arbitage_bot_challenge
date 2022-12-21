import json
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import constants
import config
from helpers.utils import get_private_key_from_mnemonic

algod_client = algod.AlgodClient(config.algod_token, config.algod_url)
account_private_key = get_private_key_from_mnemonic(
    config.account_c_mnemonic)


def create_ASA1():
    sender = config.account_c_address
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    unsigned_txn = transaction.AssetConfigTxn(
        sender=sender,
        sp=params,
        total=1000,
        default_frozen=False,
        unit_name="ISH",
        asset_name="ISHCOIN",
        manager=sender,
        reserve=sender,
        freeze=sender,
        clawback=sender,
        url="https://cmdlabs.io",
        decimals=0
    )

    print("signing txn")
    signed_txn = unsigned_txn.sign(account_private_key)

    # submit transaction
    print("sending txn")
    tx_id = algod_client.send_transactions([signed_txn])

    # wait for confirmation
    try:
        print("wait for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(
            algod_client, tx_id, 4)

        # print("Transaction information: {}".format(
        #     json.dumps(confirmed_txn, indent=4)))

        print("Created ASA index:", confirmed_txn["asset-index"])
    except Exception as err:
        print(err)


if __name__ == "__main__":
    create_ASA1()
