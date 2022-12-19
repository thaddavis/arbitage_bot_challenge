from typing import Tuple
from pyteal import *
from pyteal.ast.bytes import Bytes

from helpers import program

from .modules.constants import DO_SWAP

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():
    @Subroutine(TealType.none)
    def do_swap():
        return Seq(
            [
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: Btoi(Gtxn[1].application_args[1]),
                    TxnField.amount: Int(0),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.receiver: Global.current_application_address(),
                    TxnField.fee: Global.min_txn_fee(),
                    TxnField.close_remainder_to: Txn.sender()
                }),
                InnerTxnBuilder.Next(),  # type: ignore
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.amount: Gtxn[0].amount(),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.receiver: Gtxn[1].application_args[3],  # POOL 1
                    TxnField.fee: Global.min_txn_fee()
                }),
                InnerTxnBuilder.Submit(),
                Approve()
            ]
        )

    return program.event(
        init=Seq(Approve()),
        close_out=Seq(Approve()),
        update=Seq(Approve()),
        delete=Seq(Approve()),
        no_op=Seq(
            Cond(
                [
                    And(
                        Global.group_size() == Int(2),
                        Gtxn[0].type_enum() == TxnType.AssetTransfer,
                        Gtxn[1].type_enum() == TxnType.ApplicationCall,
                        Gtxn[1].application_args[0] == DO_SWAP,
                        # ASA1 Contract Address
                        # Txn.application_args[1] # ASA1
                        # ASA2 Contract Address
                        # Txn.application_args[2] # ASA2
                        # POOL1 Contract Address
                        # Txn.application_args[3] # POOL1
                        # POOL2 Contract Address
                        # Txn.application_args[4] # POOL 2
                    ),
                    do_swap()
                ]),
            Reject()
        )
    )


def clear():
    return Approve()
