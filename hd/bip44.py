# Copyright 2019 Juan Manuel Mera
# Distributed under the terms of GNU General Public License v3 (GPLv3)

from __future__ import annotations
import enum
from hd.bip32 import PrivateKey


class Change(enum.Enum):
    External = 0
    Internal = 1


class Coin(enum.Enum):
    Bitcoin = 0


class Wallet:
    def __init__(self, master_key: PrivateKey, coin: Coin, purpose: int):
        self.master_key = master_key
        self.coin_key = self.master_key.child(purpose, True).child(coin.value, True)
        self.account_key = None
        self.set_account(0)

    def set_account(self, account: int):
        self.account_key = self.coin_key.child(account, True)

    def address(self, index: int) -> PrivateKey:
        return self.account_key.child(Change.External.value).child(index)

    def change_address(self, index: int) -> PrivateKey:
        return self.account_key.child(Change.Internal.value).child(index)


class BitcoinWallet(Wallet):
    purpose = 44

    def __init__(self, master_key: PrivateKey, coin: Coin):
        super().__init__(master_key, coin, self.purpose)

    @classmethod
    def from_seed(cls, seed: bytes) -> BitcoinWallet:
        return cls(PrivateKey.from_seed(seed), Coin.Bitcoin)

    @classmethod
    def from_mnemonic(cls, mnemonic: bytes, passphrase: bytes = b'') -> BitcoinWallet:
        return cls(PrivateKey.from_mnemonic(mnemonic, passphrase), Coin.Bitcoin)
