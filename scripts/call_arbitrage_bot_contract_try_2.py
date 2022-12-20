from helpers.utils import format_application_info_global_state, format_application_info_global_state, get_private_key_from_mnemonic, wait_for_confirmation
import config
import json
import base64
from algosdk import account, constants, logic
from algosdk.future import transaction
from algosdk.atomic_transaction_composer import AtomicTransactionComposer, TransactionWithSigner, AccountTransactionSigner
from algosdk.v2client import algod
from algosdk.encoding import encode_address


algod_client = algod.AlgodClient(config.algod_token, config.algod_address)
sender_private_key = get_private_key_from_mnemonic(
    config.account_c_mnemonic)
ASA1_asset_id: int = config.ASA1

# TODO
# with open("../") as f:
#     js = f.read()
# c = Contract.from_json(js)


def call_arbitrage_bot_contract_try_2():

    atc = AtomicTransactionComposer()

    app_info = algod_client.application_info(config.app_id)

    creator_address = app_info['params']['creator']
    sender_address = account.address_from_private_key(
        sender_private_key)

    app_address = logic.get_application_address(config.app_id)
    print('')
    print('creator_address', creator_address)
    print('sender_address', sender_address)
    print('app_address', app_address)

    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE

    receiver = app_address
    sender = sender_address

    unsigned_txn_A = transaction.AssetTransferTxn(
        sender,  # sender (str): address of the sender
        params,  # sp (SuggestedParams): suggested params from algod
        receiver,  # receiver (str): address of the receiver
        2,  # amt (int): amount of asset base units to send
        ASA1_asset_id,  # index (int): index of the asset
    )

    signer = AccountTransactionSigner(sender_private_key)
    tws_A = TransactionWithSigner(unsigned_txn_A, signer)

    atc.add_transaction(tws_A)

    # TODO
    # atc.add_method_call(config.app_id, get_method("do_swap"), addr, sp, signer, method_args=[1,1])

    return

    app_args = [
        "DoSwap",
    ]
    unsigned_txn_B = transaction.ApplicationNoOpTxn(
        sender, params, config.app_id, app_args)

    gid = transaction.calculate_group_id([unsigned_txn_A, unsigned_txn_B])
    print('gid', gid)
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
    except Exception as err:
        print(err)


if __name__ == "__main__":
    call_arbitrage_bot_contract_try_2()
