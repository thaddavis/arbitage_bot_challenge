from algosdk.v2client import indexer, algod
from algosdk import constants
from algosdk.future import transaction
import config

from helpers.utils import get_private_key_from_mnemonic

indexer_client = indexer.IndexerClient(
    config.algod_token, config.indexer_url)
algod_client = algod.AlgodClient(config.algod_token, config.algod_url)


def delete_apps_created_by_account():
    account_private_key = get_private_key_from_mnemonic(
        config.account_a_mnemonic)
    account = config.account_a_address
    results = indexer_client.search_applications(creator=account)
    # print(results)
    apps_created = results["applications"]
    for app in apps_created:
        print(app['id'])
        params = algod_client.suggested_params()
        params.flat_fee = True
        params.fee = constants.MIN_TXN_FEE
        sender = account

        unsigned_txn = transaction.ApplicationDeleteTxn(
            sender,
            params,
            app['id']
        )

        signed_txn = unsigned_txn.sign(account_private_key)

        # submit transaction
        tx_id = algod_client.send_transactions([signed_txn])

        # step 4
        # wait for confirmation
        try:
            confirmed_txn = transaction.wait_for_confirmation(
                algod_client, tx_id, 4)

            # print("Transaction information: {}".format(
            #     json.dumps(confirmed_txn, indent=4)))
        except Exception as err:
            print(err)
