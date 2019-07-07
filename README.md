# PyHD
A simple library for hierarchically deterministic (HD) keys that implements [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki), (partially) [BIP39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) and [BIP44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki).

The objective is to have a address management in a single package.

## Usage
### BIP32
```python
from hd.bip32 import PrivateKey
mnemonic = b'yellow yellow yellow'
master_key = PrivateKey.from_mnemonic(mnemonic)
wallet_key = master_key.child_path('m/44H/0H')
first_account_key = wallet_key.child(0, True)
first_account_change_key = first_account_key.child(0)
first_address_key = first_account_change_key.child(0)
private_address = first_address_key.encode()
public_address = first_address_key.public().encode()
```

### BIP44
```python
from hd.bip44 import BitcoinWallet
mnemonic = b'yellow yellow yellow'
wallet = BitcoinWallet.from_mnemonic(mnemonic)
# wallet.set_account(0) # The account 0 is set by default
first_address_key = wallet.address(0)
private_address = first_address_key.encode()
public_address = first_address_key.public().encode()
```

## Requirements
* [coincurve](https://pypi.org/project/coincurve/)