from algosdk.v2client.indexer import IndexerClient
import config
import json
import helpers.utils

headers = {
    "X-API-Key": config.indexer_token,
}

indexer_client = IndexerClient(
    config.indexer_token,
    config.indexer_url,
    headers
)


def get_txn():
    res = indexer_client.transaction(
        'L2TZN3UVGP7PXEAHQDWSNVNPIT6HNWTSUKHFZHCMKCZBZ6I27ZQQ')

    # print('res', res)

    print("Transaction information: {}".format(
        json.dumps(res, indent=4)))


if __name__ == "__main__":
    get_txn()
