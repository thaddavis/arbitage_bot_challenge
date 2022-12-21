from algosdk.v2client import indexer, algod
import config
import json

indexer_client = indexer.IndexerClient(
    config.algod_token, config.indexer_url)

ASA1_asset_id: int = config.ASA_1
ASA2_asset_id: int = config.ASA_2

algod_client = algod.AlgodClient(config.algod_token, config.algod_url)


def print_ASA_holdings():

    print('')
    asset_info = algod_client.asset_info(ASA1_asset_id)
    results = indexer_client.accounts(asset_id=ASA1_asset_id)
    # print("assets account info: {}".format(
    #     json.dumps(results, indent=4)))
    print('asset name:', asset_info['params']['name'])
    print('')
    print('HOLDERS')
    print('')

    for account in results['accounts']:
        if ('assets' in account):
            print('address:', account['address'])
            for asset in account['assets']:
                if (asset['asset-id'] == ASA1_asset_id):
                    print('holdings are: ', asset['amount'])
                    continue
            print('')

    print('')
    asset_info = algod_client.asset_info(ASA2_asset_id)
    results = indexer_client.accounts(asset_id=ASA2_asset_id)
    # print("assets account info: {}".format(
    #     json.dumps(results, indent=4)))
    print('asset name:', asset_info['params']['name'])
    print('')
    print('HOLDERS')
    print('')

    for account in results['accounts']:
        if ('assets' in account):
            print('address:', account['address'])
            for asset in account['assets']:
                if (asset['asset-id'] == ASA2_asset_id):
                    print('holdings are: ', asset['amount'])
                    continue
            print('')
