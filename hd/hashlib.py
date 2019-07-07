# Copyright 2019 Juan Manuel Mera
# Distributed under the terms of GNU General Public License v3 (GPLv3)

import hmac
from hashlib import sha256, pbkdf2_hmac, new as hash_new


def double_sha256(payload: bytes) -> bytes:
    return sha256(sha256(payload).digest()).digest()


def hmac_sha512(key: bytes, msg: bytes) -> bytes:
    return hmac.digest(key, msg, 'sha512')


def pbkdf2_sha512(password: bytes, salt: bytes, iterations: int, dklen: int) -> bytes:
    return pbkdf2_hmac('sha512', password, salt, iterations, dklen)


def hash160(payload: bytes) -> bytes:
    return hash_new('ripemd160', sha256(payload).digest()).digest()
