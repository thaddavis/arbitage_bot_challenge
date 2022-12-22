from typing import Tuple
from pyteal import *
from pyteal.ast.bytes import Bytes

from helpers import program

from .modules.constants import DO_SWAP, OPTIN_CONTRACT_TO_ASAS, OPTOUT_CONTRACT_TO_ASAS, CLOSE_OUT_CONTRACT_BALANCE, RETURN_ASA_1_TO_SENDER

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():
    @Subroutine(TealType.none)
    def do_swap():
        return Seq([
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                # ASA1 asset id
                TxnField.xfer_asset: Btoi(Gtxn[1].application_args[1]),
                # Amount of ASA1 sent to this contract is now being sent to POOL 1
                TxnField.asset_amount: Gtxn[0].asset_amount(),
                TxnField.sender: Global.current_application_address(),
                # POOL 1 address
                TxnField.asset_receiver: Gtxn[1].application_args[4],
                TxnField.fee: Int(0)
            }),
            InnerTxnBuilder.Next(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                # POOL 1 app-id
                TxnField.application_id: Btoi(Gtxn[1].application_args[3]),
                TxnField.on_completion: OnComplete.NoOp,
                TxnField.sender: Global.current_application_address(),
                TxnField.fee: Int(0),
                TxnField.application_args: [
                    # [7] is the amount of the pair you want from the pool in exchange for the tokens sent in previous txn
                    Bytes("SWAP"), Gtxn[1].application_args[7]],
                TxnField.assets: [Btoi(Gtxn[1].application_args[1]), Btoi(
                    Gtxn[1].application_args[2])],  # ASA1 and ASA2
                TxnField.applications: [
                    Btoi(Gtxn[1].application_args[3])]  # app-id of POOL 1
            }),
            InnerTxnBuilder.Submit(),
            # V2 - Final Solution - Test out Pact.fi API
            # InnerTxn to call POOL1 and swap ASA1 for ASA2 # WORKS
            # InnerTxn to call POOL2 and swap ASA2 for ASA1 # TODO
            # InnerTxn to send ASA1 to Sender # TODO
            Approve()
        ])

    @ Subroutine(TealType.none)
    def return_asa_1_to_sender():
        return Seq([
            # V1 - Transfer ASA1 back to sender
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: Btoi(Gtxn[1].application_args[1]),
                # vvv simulate amount of ASA 1 to return to sender vvv
                TxnField.asset_amount: Btoi(Gtxn[1].application_args[2]),
                TxnField.sender: Global.current_application_address(),
                TxnField.asset_receiver: Gtxn[1].sender(),
                TxnField.fee: Int(0),
            }),
            InnerTxnBuilder.Submit(),
            Approve()
        ])

    @ Subroutine(TealType.none)
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

    @ Subroutine(TealType.none)
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

    @ Subroutine(TealType.none)
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
                        Gtxn[1].type_enum() == TxnType.ApplicationCall,
                        Gtxn[1].application_args[0] == DO_SWAP
                    ),
                    # ASA1
                    # Txn.application_args[1] # ASA1 asset id
                    # ASA2
                    # Txn.application_args[2] # ASA2 asset id
                    # POOL1
                    # Txn.application_args[3] # POOL 1 app id
                    # POOL1
                    # Txn.application_args[4] # POOL 1 address
                    # POOL2
                    # Txn.application_args[5] # POOL 2 app id
                    # POOL2
                    # Txn.application_args[6] # POOL 2 address
                    # Amount of the pair you want from the pool in exchange for the ASA tokens arriving in Gtxn[0]
                    # Txn.application_args[7] # uint64  amount of pair token you want from the pool
                    do_swap()
                ],
                [
                    And(
                        Global.group_size() == Int(2),
                        Gtxn[0].type_enum() == TxnType.AssetTransfer,
                        Gtxn[1].application_args[0] == RETURN_ASA_1_TO_SENDER
                    ),
                    # ASA1 Contract Address
                    # Txn.application_args[1] # ASA1 asset id
                    # Txn.application_args[2] # Amount of ASA1 to return to sender
                    return_asa_1_to_sender()
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
