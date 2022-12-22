from base64 import b64decode


def decode_SWAP_txn_args():
    # arg2 = "AAAAAABMPVk="
    arg2 = "AAAAAAAAAAE="

    print('arg2', arg2)
    # print('arg2 decoded', int.from_bytes(arg2, byteorder='big'))

    # '20195413974224244067305679677'

    print(b64decode(arg2))
    print(int.from_bytes(b64decode(arg2), byteorder='big'))

    # val = 1337
    # encoded = (val).to_bytes(8, 'big')
    # decoded = int.from_bytes(encoded, byteorder='big')
    # print('test val encoded', encoded)
    # print('test val decoded', decoded)


if __name__ == "__main__":
    decode_SWAP_txn_args()
