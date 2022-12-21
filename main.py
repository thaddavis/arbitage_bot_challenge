import sys
from scripts.list_apps_created_by_account import list_apps_created_by_account
from scripts.delete_apps_created_by_account import delete_apps_created_by_account
from scripts.call_arbitrage_bot_contract import call_arbitrage_bot_contract
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
from scripts.optout_contract_to_ASAs import optout_contract_to_ASAs

if __name__ == "__main__":

    print('sys.argv[i]', sys.argv[1])

    match sys.argv[1]:
        case 'print_ASA_holdings':
            print('** print_ASA_holdings **')
            print_ASA_holdings()
        case 'create_ASA1':
            print('** create_ASA1 **')
        case _:
            print('Default Behavior')

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
