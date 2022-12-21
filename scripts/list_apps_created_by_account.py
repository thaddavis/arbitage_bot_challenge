from algosdk.v2client import indexer
import config


indexer_client = indexer.IndexerClient(
    config.indexer_token, config.indexer_url)


def list_apps_created_by_account():
    account = config.account_a_address
    results = indexer_client.search_applications(creator=account)
    # print(results)
    apps_created = results["applications"]
    for app in apps_created:
        print(app['id'])
