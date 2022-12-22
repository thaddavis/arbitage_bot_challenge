from algosdk.v2client import algod
import config

algod_client = algod.AlgodClient(
    config.algod_token, config.algod_url, config.algod_headers)
