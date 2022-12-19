# Arbitage Bot Challenge

## TLDR

Coding Challenge presented by Ludovit Sholz and Laurens Michiels van Kessenich to Tad Duval on Dec. 19th at 10:00am EST

## Prompt

Write a smart contract in PyTeal which has an input group of 2 transactions.

- Gtxn[0] is Asset transfer (ASA1) to the contract address
- Gtxn[1] is Noop app call - "DoSwap" with the following application_args...
    - constant DoSwap
    - ASA1
    - ASA2
    - POOL1 [3]
    - POOL2 [4]

"DoSwap" will make the following inner txn calls

    - Inner Txn #1) call pact.fi POOL1 and pay ASA1 to receive ASA2.
    - Inner Txn #2) call pact.fi POOL2 and pay received ASA2 from previous tx and receives ASA1
    - Inner Txn #3) send ASA1 back to sender who initiated the "DoSwap" function
