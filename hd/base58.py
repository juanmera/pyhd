# Copyright 2019 Juan Manuel Mera
# Distributed under the terms of GNU General Public License v3 (GPLv3)

from hd.hashlib import double_sha256

BASE = 58
CHECKSUM_LEN = 4
CODE_STRING = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def raw_encode(payload: bytes) -> bytes:
    x = int.from_bytes(payload, 'big')
    out = bytearray()
    while x > 0:
        x, r = divmod(x, BASE)
        out.append(CODE_STRING[r])
    for c in payload:
        if c > 0:
            break
        out.append(CODE_STRING[0])
    out.reverse()
    return bytes(out)


def raw_decode(payload: bytes) -> bytes:
    x = 0
    zeros = 0
    for i in payload:
        r = CODE_STRING.index(i)
        if r == 0 and x == 0:
            zeros += 1
        else:
            x = x * BASE + r
    out = x.to_bytes((x.bit_length()+7)//8, 'big')
    return b'\x00' * zeros + out


def checksum(payload: bytes) -> bytes:
    return double_sha256(payload)[:CHECKSUM_LEN]


def encode(payload: bytes) -> bytes:
    return raw_encode(payload + checksum(payload))


def decode(payload: bytes) -> bytes:
    decoded = raw_decode(payload)
    if decoded[-CHECKSUM_LEN:] != checksum(decoded[:-CHECKSUM_LEN]):
        raise ValueError('invalidChecksum')
    return decoded
