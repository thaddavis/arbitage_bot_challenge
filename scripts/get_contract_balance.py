from algosdk.v2client import algod
from algosdk import logic
import config
import json

algod_client = algod.AlgodClient(
    config.algod_token, config.algod_url, config.algod_headers)


def get_contract_balance():

    print("app_id:", config.app_id)
    application_address = logic.get_application_address(config.app_id)
    print("application address for app_id", application_address)
    print('')

    account_info = algod_client.account_info(application_address)
    print("Account Info: {}".format(
        json.dumps(account_info, indent=4)))
