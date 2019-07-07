# Copyright 2019 Juan Manuel Mera
# Distributed under the terms of GNU General Public License v3 (GPLv3)

from hd.hashlib import pbkdf2_sha512

PASSPHRASE_BASE = b'mnemonic'
PBKDF2_ITERATIONS = 2048
SEED_LEN = 64


def to_seed(mnemonic: bytes, passphrase: bytes=b'') -> bytes:
    # TODO: Normalize mnemonic and passphrase
    return pbkdf2_sha512(mnemonic, PASSPHRASE_BASE + passphrase, PBKDF2_ITERATIONS, SEED_LEN)