# Arbitage Bot Challenge

## TLDR

Coding Challenge presented by Ludovit Sholz and Laurens Michiels van Kessenich to Tad Duval on Dec. 19th at 10:00am EST

## Prompt

Write a smart contract in PyTeal which has an input group of 2 transactions.

- Gtxn[0] is Asset transfer (ASA1) to the contract address
- Gtxn[1] is Noop app call - "DoSwap" with the following args...
    - [0] constant DoSwap
    - [1] ASA1
    - [2] ASA2
    - [3] POOL1
    - [4] POOL2

"DoSwap" will make the following inner txn calls

    - Inner Txn #1) call pact.fi POOL1 and pay ASA1 to receive ASA2.
    - Inner Txn #2) call pact.fi POOL2 and pay received ASA2 from previous tx and receives ASA1
    - Inner Txn #3) send ASA1 back to sender who initiated the "DoSwap" function

## Additional Reference material

`https://testnet.algoexplorer.io/tx/group/BHXv3MOJdEvoBexjdpK92VG4nOV2EmkOV2XZHxTLRyQ%3D`
`https://testnet.algoexplorer.io/tx/GEXCU3RTRTRJDUC6Q55ACFHII2MPDDCY76TLPPLFQDD7UKLDQRBA`
`https://pyteal.readthedocs.io/en/stable/index.html`
`https://www.pact.fi/`
`https://folks.finance/`

## Getting Started

Check out the following files in the READMEs folder in this order...

- README.sandbox.md
- README.setup_python.md
- README.build_and_deploy.md

## Tips and Tricks

Check out the various  files in the READMEs folder
