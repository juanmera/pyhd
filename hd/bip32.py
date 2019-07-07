# Copyright 2019 Juan Manuel Mera
# Distributed under the terms of GNU General Public License v3 (GPLv3)

from __future__ import annotations
import abc
import enum
import coincurve as cc
from typing import Tuple, Union
from hd.hashlib import hmac_sha512, hash160
from hd import base58, bip39

BLOCK_LEN = 32
FINGERPRINT_LEN = 4
HARDENED_CHILD_ID = 2**31
SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
MASTER_HMAC_KEY = b'Bitcoin seed'
MASTER_FINGERPRINT = b'\x00\x00\x00\x00'


class Version(enum.Enum):
    PubKeyHash = b'\x00'
    ScriptHash = b'\x05'
    PrivateKey = b'\x80'
    Bip32Private = b'\x04\x88\xAD\xE4'
    Bip32Public = b'\x04\x88\xB2\x1E'


class Key(abc.ABC):
    version = None

    def __init__(self, key: Union[cc.PrivateKey, cc.PublicKey], chain: bytes, parent_fingerprint: bytes, depth: int=0, index: int=0):
        self.key = key
        self.chain = chain
        self.parent_fingerprint = parent_fingerprint
        self.depth = depth
        self.index = index

    def serialize(self) -> bytes:
        return base58.encode(self.version + self.depth.to_bytes(1, 'big') + self.parent_fingerprint + self.index.to_bytes(4, 'big') + self.chain + self.format())

    @abc.abstractmethod
    def format(self) -> bytes:
        pass

    @abc.abstractmethod
    def hash160(self) -> bytes:
        pass

    def _fingerprint(self) -> bytes:
        return self.hash160()[:FINGERPRINT_LEN]


class PublicKey(Key):
    version = Version.Bip32Public.value

    def child(self, i: int) -> PublicKey:
        if i >= HARDENED_CHILD_ID:
            raise Exception('cannotCreateChildFromPublicHardenedKey')
        ll, lr = hmac_derive(self.chain, self.key.format() + i.to_bytes(4, 'big'))
        return PublicKey(cc.PublicKey.from_secret(ll).combine(self.key), lr, self._fingerprint(), self.depth + 1, i)

    def hash160(self) -> bytes:
        return hash160(self.format())

    def format(self) -> bytes:
        return self.key.format()

    def encode(self) -> bytes:
        return base58.encode(Version.PubKeyHash.value + self.hash160())


class PrivateKey(Key):
    version = Version.Bip32Private.value

    @classmethod
    def from_seed(cls, seed: bytes) -> PrivateKey:
        ll, lr = hmac_derive(MASTER_HMAC_KEY, seed)
        return cls(cc.PrivateKey(ll), lr, MASTER_FINGERPRINT)

    @classmethod
    def from_mnemonic(cls, mnemonic: bytes, passphrase: bytes=b'') -> PrivateKey:
        return cls.from_seed(bip39.to_seed(mnemonic, passphrase))

    def child(self, i: int, hardened: bool=False) -> PrivateKey:
        if hardened:
            i += HARDENED_CHILD_ID
        if i >= HARDENED_CHILD_ID:
            ll, lr = hmac_derive(self.chain, self.format() + i.to_bytes(4, 'big'))
        else:
            ll, lr = hmac_derive(self.chain, self.key.public_key.format() + i.to_bytes(4, 'big'))
        secret = (int.from_bytes(ll, 'big') + self.key.to_int()) % SECP256K1_N
        return PrivateKey(cc.PrivateKey(secret.to_bytes(32, 'big')), lr, self._fingerprint(), self.depth + 1, i)

    def child_path(self, path: str) -> PrivateKey:
        indexes = path.split('/')
        indexes.pop(0)
        out = self
        for index in indexes:
            hardened = index[-1].upper() == 'H'
            if hardened:
                index = index[:-1]
            out = out.child(int(index, 10), hardened)
        return out

    def public(self) -> PublicKey:
        return PublicKey(self.key.public_key, self.chain, self.parent_fingerprint, self.depth, self.index)

    def hash160(self) -> bytes:
        return hash160(self.key.public_key.format())

    def format(self):
        return b'\x00' + self.key.secret

    def encode(self) -> bytes:
        return base58.encode(Version.PrivateKey.value + self.key.secret + b'\x01')


def hmac_derive(key: bytes, msg: bytes) -> Tuple[bytes, bytes]:
    l = hmac_sha512(key, msg)
    return l[:BLOCK_LEN], l[BLOCK_LEN:]


