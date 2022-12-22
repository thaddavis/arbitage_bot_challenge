# Test final solution

All scripts are triggered through `python main.py`

## build and deploy contract

- ./build.sh contracts.arbitrage_bot.contract && python deploy.py

## Flow

- Create ASAs
    run `./scripts/create_ASA1.py`
    run `./scripts/create_ASA2.py`
- View ASA Holders
    run `./scripts/print_ASA_holdings.py`
- Optin to ASAs
    run `./scripts/optin_contract_to_ASAs.py`
- View ASA Holders
    run `./scripts/print_ASA_holdings.py`
- Optin DoSwap caller to ASA1
    run `./scripts/optin_account_to_ASA.py`
- View ASA Holders
    run `./scripts/print_ASA_holdings.py`
- Transfer 20 tokens to the DoSwap caller
    run `./scripts/transfer_ASA_amount_to_account.py`
- View ASA Holders again
    run `./scripts/print_ASA_holdings.py`
- Call the DoSwap function - Move tokens in and out
    `python main.py call_contract_testnet`
- Opt-out of ASAs
    run `./scripts/optout_contract_to_ASAs.py`