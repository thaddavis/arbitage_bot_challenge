from algosdk.v2client import indexer, algod
import config
import json

indexer_client = indexer.IndexerClient(
    config.algod_token, config.indexer_address)

ASA1_asset_id: int = config.ASA1
ASA2_asset_id: int = config.ASA2

algod_client = algod.AlgodClient(config.algod_token, config.algod_address)


def print_ASA_holdings():
    results = indexer_client.accounts(asset_id=ASA1_asset_id)

    # print("assets account info: {}".format(
    #     json.dumps(results, indent=4)))

    print('')
    asset_info = algod_client.asset_info(ASA1_asset_id)
    print('asset name:', asset_info['params']['name'])
    print('')
    print('HOLDERS')
    print('')

    for account in results['accounts']:
        print('address:', account['address'])
        for asset in account['assets']:
            if (asset['asset-id'] == ASA1_asset_id):
                print('holdings are: ', asset['amount'])
                continue
        print('')

    print('')
    asset_info = algod_client.asset_info(ASA2_asset_id)
    print('asset name:', asset_info['params']['name'])
    print('')
    print('HOLDERS')
    print('')

    for account in results['accounts']:
        print('address:', account['address'])
        for asset in account['assets']:
            if (asset['asset-id'] == ASA1_asset_id):
                print('holdings are: ', asset['amount'])
                continue
        print('')
