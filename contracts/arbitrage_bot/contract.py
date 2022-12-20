from typing import Tuple
from pyteal import *
from pyteal.ast.bytes import Bytes

from helpers import program

from .modules.constants import DO_SWAP, OPTIN_CONTRACT_TO_ASAS

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():
    @Subroutine(TealType.none)
    def do_swap():
        return Seq([
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

    return program.event(
        init=Seq(Approve()),
        close_out=Seq(Approve()),
        update=Seq(Approve()),
        delete=Seq(Approve()),
        no_op=Seq(
            Cond(
                [
                    Txn.application_args[0] == DO_SWAP,
                    # ASA1 Contract Address
                    # Txn.application_args[1] # ASA1
                    # ASA2 Contract Address
                    # Txn.application_args[2] # ASA2
                    # POOL1 Contract Address
                    # Txn.application_args[3] # POOL1
                    # POOL2 Contract Address
                    # Txn.application_args[4] # POOL 2
                    do_swap()
                ],
                [
                    And(
                        Global.group_size() == Int(2),
                        Gtxn[0].type_enum() == TxnType.Payment,
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
