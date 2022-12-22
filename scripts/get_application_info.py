from algosdk.v2client import algod
from algosdk import logic
import config

algod_client = algod.AlgodClient(
    config.algod_token, config.algod_url, config.algod_headers)


def get_application_info():

    print("app_id:", config.app_id)
    print("application address for app_id",
          logic.get_application_address(config.app_id))
    print('')

    print("pool_1_app_id:", config.pool_1_app_id)
    print("application address for pool_1_app_id",
          logic.get_application_address(config.pool_1_app_id))
    print('')
    # response = algod_client.application_info(config.pool_1_app_id)
    # print(response)

    print("pool_2_app_id:", config.pool_2_app_id)
    print("application address for pool_2_app_id",
          logic.get_application_address(config.pool_2_app_id))
    print('')

    # response = algod_client.application_info(config.pool_1_app_id)
    # print(response)
