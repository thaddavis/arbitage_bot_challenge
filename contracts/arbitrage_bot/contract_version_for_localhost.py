from typing import Tuple
from pyteal import *
from pyteal.ast.bytes import Bytes

from helpers import program

from .modules.constants import DO_SWAP, OPTIN_CONTRACT_TO_ASAS, OPTOUT_CONTRACT_TO_ASAS, CLOSE_OUT_CONTRACT_BALANCE

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():
    @Subroutine(TealType.none)
    def do_swap():
        return Seq([
            # V1 - Transfer ASA1 back to sender
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Btoi(Gtxn[1].application_args[1]),  # ASA1
                # vvv simulate amount of ASA 1 to return to sender vvv
                TxnField.asset_amount: Btoi(Gtxn[1].application_args[5]),
                TxnField.sender: Global.current_application_address(),
                TxnField.asset_receiver: Gtxn[1].sender(),
                TxnField.fee: Int(0),
            }),
            InnerTxnBuilder.Submit(),
            # V2 - Final Solution - Test out Pact.fi API
            # InnerTxn to call POOL1 and swap ASA1 for ASA2
            # InnerTxn to call POOL2 and swap ASA2 for ASA1
            # InnerTxn to send ASA1 to Sender
            Approve()
        ])

    @Subroutine(TealType.none)
    def optin_contract_to_asas():
        return Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Btoi(Gtxn[1].application_args[1]),  # ASA1
                TxnField.asset_amount: Int(0),
                TxnField.sender: Global.current_application_address(),
                TxnField.asset_receiver: Global.current_application_address(),
                TxnField.fee: Int(0),
            }),
            InnerTxnBuilder.Next(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Btoi(Gtxn[1].application_args[2]),  # ASA2
                TxnField.asset_amount: Int(0),
                TxnField.sender: Global.current_application_address(),
                TxnField.asset_receiver: Global.current_application_address(),
                TxnField.fee: Int(0),
            }),
            InnerTxnBuilder.Submit(),
            Approve()
        ])

    @Subroutine(TealType.none)
    def optout_contract_to_asas():
        return Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Btoi(Txn.application_args[1]),  # ASA1
                TxnField.asset_close_to: Global.current_application_address(),
                TxnField.sender: Global.current_application_address(),
                TxnField.asset_receiver: Global.current_application_address(),
                TxnField.fee: Int(0)
            }),
            InnerTxnBuilder.Next(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Btoi(Txn.application_args[2]),  # ASA2
                TxnField.asset_close_to: Global.current_application_address(),
                TxnField.sender: Global.current_application_address(),
                TxnField.asset_receiver: Global.current_application_address(),
                TxnField.fee: Int(0)
            }),
            InnerTxnBuilder.Submit(),
            Approve()
        ])

    @Subroutine(TealType.none)
    def close_out_contract_balance():
        return Seq(
            [
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.amount: Balance(Global.current_application_address()) - Global.min_txn_fee(),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.receiver: Txn.sender(),
                    TxnField.fee: Global.min_txn_fee(),
                    TxnField.close_remainder_to: Txn.sender()
                }),
                InnerTxnBuilder.Submit(),
                Approve()
            ]
        )

    return program.event(
        init=Seq(Approve()),
        close_out=Seq(Approve()),
        update=Seq(Approve()),
        delete=If(Balance(Global.current_application_address()) == Int(0))
        .Then(Approve())
        .Else(Reject()),
        no_op=Seq(
            Cond(
                [
                    Txn.application_args[0] == OPTOUT_CONTRACT_TO_ASAS,
                    # ASA1 Contract Address
                    # Txn.application_args[1] # ASA1
                    # ASA2 Contract Address
                    # Txn.application_args[2] # ASA2
                    optout_contract_to_asas()
                ],
                [
                    And(
                        Global.group_size() == Int(2),
                        Gtxn[0].type_enum() == TxnType.AssetTransfer,
                        Gtxn[1].application_args[0] == DO_SWAP
                    ),
                    # ASA1 Contract Address
                    # Txn.application_args[1] # ASA1 asset id
                    # ASA2 Contract Address
                    # Txn.application_args[2] # ASA2 asset id
                    # POOL1 Contract Address
                    # Txn.application_args[3] # POOL1 address
                    # POOL2 Contract Address
                    # Txn.application_args[4] # POOL 2 address
                    # Amount of ASA1 to return to sender
                    # Txn.application_args[5] # uint64
                    do_swap()
                ],
                [
                    Txn.application_args[0] == CLOSE_OUT_CONTRACT_BALANCE,
                    close_out_contract_balance()
                ],
                [
                    And(
                        Global.group_size() == Int(2),
                        Gtxn[0].type_enum() == TxnType.Payment,
                        Gtxn[1].type_enum() == TxnType.ApplicationCall,
                        Gtxn[1].application_args[0] == OPTIN_CONTRACT_TO_ASAS
                    ),
                    # ASA1 Contract Address
                    # Txn.application_args[1] # ASA1
                    # ASA2 Contract Address
                    # Txn.application_args[2] # ASA2
                    optin_contract_to_asas()
                ]
            ),
            Reject()
        )
    )


def clear():
    return Approve()
