import sys
from scripts.get_application_info import get_application_info
from scripts.list_apps_created_by_account import list_apps_created_by_account
from scripts.delete_apps_created_by_account import delete_apps_created_by_account
from scripts.call_contract_localhost import call_contract_localhost
from scripts.call_contract_testnet import call_contract_testnet
from scripts.create_ASA1 import create_ASA1
from scripts.create_ASA2 import create_ASA2
from scripts.optin_account_to_ASA import optin_account_to_ASA
from scripts.get_assets_info_of_account import get_assets_info_of_account
from scripts.transfer_ASA_amount_to_account import transfer_ASA_amount_to_account
from scripts.print_ASA_holdings import print_ASA_holdings
from scripts.transfer_ASA_amount_to_contract import transfer_ASA_amount_to_contract
from scripts.optin_contract_to_ASAs import optin_contract_to_ASAs
from scripts.pact_experiment import pact_experiment
from scripts.get_txn import get_txn
from scripts.optout_contract_from_ASAs import optout_contract_from_ASAs
from scripts.decode_SWAP_txn_args import decode_SWAP_txn_args
from scripts.get_contract_balance import get_contract_balance

if __name__ == "__main__":

    if len(sys.argv) > 1:
        print('sys.argv[i]', sys.argv[1])

        match sys.argv[1]:
            case 'print_ASA_holdings':
                print_ASA_holdings()
            case 'create_ASA1':
                pass
            case 'get_application_info':
                get_application_info()
            case 'get_contract_balance':
                get_contract_balance()
            case 'call_contract_testnet':
                call_contract_testnet()
            case 'optin_contract_to_ASAs':
                optin_contract_to_ASAs()
            case 'optin_account_to_ASA':
                optin_account_to_ASA()
            case 'optout_contract_from_ASAs':
                optout_contract_from_ASAs()
            case 'decode_SWAP_txn_args':
                decode_SWAP_txn_args()
            case _:
                print('Unsupported script')
    else:
        get_application_info()
        # list_apps_created_by_account()
        # delete_apps_created_by_account()
        # transfer_ASA1_to_arbitrage_bot()
        # create_ASA1()
        # create_ASA2()
        # optin_account_to_ASA()
        # get_assets_info_of_account()
        # print_ASA_holdings()
        # transfer_ASA_amount_to_account()
        # transfer_ASA_amount_to_contract()
        # call_arbitrage_bot_contract()
        # call_arbitrage_bot_contract_try_2()
        # optin_contract_to_asas()
        # pact_experiment()
        # get_txn()
        # optout_contract_to_ASAs()

        # --- Final Test Flow ---
        # optin_contract_to_ASAs()
        # optin_account_to_ASA()
        # transfer_ASA_amount_to_account()
        # call_arbitrage_bot_contract()
