from algosdk.v2client.algod import AlgodClient
import pactsdk
import config

headers = {
    "X-API-Key": config.testnet_algod_token,
}

algod_client = AlgodClient(
    config.testnet_algod_token,
    config.testnet_algod_server,
    headers
)

pact = pactsdk.PactClient(
    algod_client, pact_api_url="https://api.testnet.pact.fi"
)


def pact_experiment():
    algo = pact.fetch_asset(0)
    other_coin = pact.fetch_asset(19386116)

    print('algo', algo)
    print('other_coin', other_coin)

    # The pool will be fetched regardless of assets order.
    pools = pact.fetch_pools_by_assets(algo, other_coin)

    # pools = pact.list_pools()
    print('pools', pools)
    pool = pact.fetch_pool_by_id(56999273)
    print('pool', pool)
