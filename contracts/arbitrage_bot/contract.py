from multiprocessing.sharedctypes import Value
from typing import Tuple
from more_itertools import last
from pyteal import *
from pyteal.ast.bytes import Bytes

from helpers import program

from .modules.constants import DO_SWAP, OPTIN_CONTRACT_TO_ASAS, OPTOUT_CONTRACT_TO_ASAS, CLOSE_OUT_CONTRACT_BALANCE, RETURN_ASA_1_TO_SENDER

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():
    # old config
    #
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
    #
    # New config
    # in appcall one can reference applications - pools through he wants to swap
    # he can reference 2 to 3 pools
    # Txn.application_args[0] = DoSwap
    @Subroutine(TealType.none)
    def do_swap():

        return Seq(
            # 4,672,586,512
            swap1a := App.globalGetEx(Txn.applications[0], Bytes("A")),
            Assert(swap1a.hasValue()),
            # 468,518,264,281
            swap1b := App.globalGetEx(Txn.applications[0], Bytes("B")),
            Assert(swap1b.hasValue()),
            swap1config := App.globalGetEx(Txn.applications[0], Bytes("CONFIG")),
            Assert(swap1config.hasValue()),
            # 1E1AB70 31566704
            swap1assetA := Btoi(Substring(swap1config.value(), Int(0), Int(8))),
            # 1af71298 452399768
            swap1assetB := Btoi(Substring(swap1config.value(), Int(8), Int(16))),

            If(swap1assetA == Gtxn[0].xfer_asset()).Then(Seq(
                asaToSendAtSwap1 := swap1assetA,
                asaToReceiveAtSwap1 := swap1assetB,
                amountToReceiveAtSwap1 := Gtxn[0].asset_amount() * swap1b.value() / swap1a.value() - Int(1),
            )).Else(Seq(
                Assert(swap1assetB == Gtxn[0].xfer_asset()),
                asaToSendAtSwap1 := swap1assetB,
                asaToReceiveAtSwap1 := swap1assetA,
                amountToReceiveAtSwap1 := Gtxn[0].asset_amount() * swap1a.value() / swap1b.value() - Int(1),
            )),

            # Assert(config.index)
            #
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                # ASA1 asset id
                TxnField.xfer_asset: asaToSendAtSwap1,
                # Amount of ASA1 sent to this contract is now being sent to POOL 1
                TxnField.asset_amount: Gtxn[0].asset_amount(),
                TxnField.sender: Global.current_application_address(),
                # POOL 1 address
                # pool 1 address
                TxnField.asset_receiver: AppParam.address(Txn.applications[0]),
                TxnField.fee: Int(1000)
            }),
            InnerTxnBuilder.Next(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                # POOL 1 app-id
                # pool 1
                TxnField.application_id: Txn.applications[0],  # pool 1 app id
                TxnField.on_completion: OnComplete.NoOp,
                TxnField.sender: Global.current_application_address(),
                TxnField.fee: Int(2000),
                TxnField.application_args: [
                    Bytes("SWAP"),
                    Itob(amountToReceiveAtSwap1)
                ],
                TxnField.assets: [
                    asaToSendAtSwap1,   # usdc
                    asaToReceiveAtSwap1  # vote
                ],
                TxnField.applications: [
                    Txn.applications[0]  # pool 1 app id
                ]
            }),
            InnerTxnBuilder.Submit(),


            # 4,672,586,512
            swap2a := App.globalGetEx(Txn.applications[1], Bytes("A")),
            Assert(swap2a.hasValue()),
            # 468,518,264,281
            swap2b := App.globalGetEx(Txn.applications[1], Bytes("B")),
            Assert(swap2b.hasValue()),
            swap2config := App.globalGetEx(Txn.applications[1], Bytes("CONFIG")),
            Assert(swap2config.hasValue()),
            # 1E1AB70 31566704
            swap2assetA := Btoi(Substring(swap2config.value(), Int(0), Int(8))),
            # 1af71298 452399768
            swap2assetB := Btoi(Substring(swap2config.value(), Int(8), Int(16))),

            afterSwap1Balance := AssetHolding.balance(
                Global.current_application_address(),
                asaToReceiveAtSwap1
            ),

            If(swap2assetA == asaToReceiveAtSwap1).Then(Seq(
                asaToSendAtSwap2 := swap2assetA,
                asaToReceiveAtSwap2 := swap2assetB,
                amountToReceiveAtSwap2 := afterSwap1Balance.value() * swap2b.value() / swap2a.value() - Int(1),
            )).Else(Seq(
                Assert(swap2assetB == Gtxn[0].xfer_asset()),
                asaToSendAtSwap2 := swap2assetB,
                asaToReceiveAtSwap2 := swap2assetA,
                amountToReceiveAtSwap2 := afterSwap1Balance.value() * swap2a.value() / swap2b.value() - Int(1),
            )),
            lastAsset := asaToReceiveAtSwap2,


            # Assert(config.index)
            #
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: asaToSendAtSwap2,
                TxnField.asset_amount: afterSwap1Balance,
                TxnField.sender: Global.current_application_address(),
                # pool 2 address id
                TxnField.asset_receiver: AppParam.address(Txn.applications[1]),
                TxnField.fee: Int(1000)
            }),
            InnerTxnBuilder.Next(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.ApplicationCall,
                TxnField.application_id: Txn.applications[1],  # pool 2 app id
                TxnField.on_completion: OnComplete.NoOp,
                TxnField.sender: Global.current_application_address(),
                TxnField.fee: Int(2000),
                TxnField.application_args: [
                    Bytes("SWAP"),
                    Itob(amountToReceiveAtSwap2)
                ],
                TxnField.assets: [
                    asaToSendAtSwap2,    # vote
                    asaToReceiveAtSwap2  # usdt
                ],
                TxnField.applications: [
                    Txn.applications[1]  # pool 2 app id
                ]
            }),
            InnerTxnBuilder.Submit(),

            If(Txn.applications.length() >= Int(3), Seq(

                swap3a := App.globalGetEx(Txn.applications[1], Bytes("A")),
                Assert(swap3a.hasValue()),
                swap3b := App.globalGetEx(Txn.applications[1], Bytes("B")),
                Assert(swap3b.hasValue()),
                swap3config := App.globalGetEx(Txn.applications[1], Bytes("CONFIG")),
                Assert(swap3config.hasValue()),
                # 1E1AB70 31566704
                swap3assetA := Btoi(Substring(swap3config.value(), Int(0), Int(8))),
                # 1af71298 452399768
                swap3assetB := Btoi(Substring(swap3config.value(), Int(8), Int(16))),

                afterswap2Balance := AssetHolding.balance(
                    Global.current_application_address(),
                    asaToReceiveAtSwap2
                ),

                If(swap3assetA == asaToReceiveAtSwap2).Then(Seq(
                    asaToSendAtswap3 := swap3assetA,
                    asaToReceiveAtswap3 := swap3assetB,
                    amountToReceiveAtswap3 := afterswap2Balance.value() * swap3b.value() / swap3a.value() - Int(1),
                )).Else(Seq(
                    Assert(swap3assetB == Gtxn[0].xfer_asset()),
                    asaToSendAtswap3 := swap3assetB,
                    asaToReceiveAtswap3 := swap3assetA,
                    amountToReceiveAtswap3 := afterswap2Balance.value() * swap3a.value() / swap3b.value() - Int(1),
                )),
                lastAsset := amountToReceiveAtswap3,


                # Assert(config.index)
                #
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: asaToSendAtswap3,
                    TxnField.asset_amount: afterswap2Balance,
                    TxnField.sender: Global.current_application_address(),
                    # pool 2 address id
                    TxnField.asset_receiver: AppParam.address(Txn.applications[2]),
                    TxnField.fee: Int(1000)
                }),
                InnerTxnBuilder.Next(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.ApplicationCall,
                    # pool 2 app id
                    TxnField.application_id: Txn.applications[2],
                    TxnField.on_completion: OnComplete.NoOp,
                    TxnField.sender: Global.current_application_address(),
                    TxnField.fee: Int(2000),
                    TxnField.application_args: [
                        Bytes("SWAP"),
                        Itob(amountToReceiveAtswap3)
                    ],
                    TxnField.assets: [
                        asaToSendAtswap3,    # usdt
                        asaToReceiveAtswap3  # usdc
                    ],
                    TxnField.applications: [
                        Txn.applications[2]  # pool 2 app id
                    ]
                }),
                InnerTxnBuilder.Submit(),
                # Assert(config.index)
                #
            )),

            lastAssetBalance := AssetHolding.balance(
                Global.current_application_address(),
                lastAsset
            ),
            Assert(lastAsset == Gtxn[0].xfer_asset()),
            Assert(lastAssetBalance > Gtxn[0].amount()),

            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: lastAsset,
                TxnField.asset_amount: lastAssetBalance,
                TxnField.sender: Global.current_application_address(),
                TxnField.asset_receiver: Gtxn[0].sender(),
                TxnField.fee: Int(1000)
            }),
            InnerTxnBuilder.Submit(),


            Approve()
        )

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
