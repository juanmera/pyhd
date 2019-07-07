# Copyright 2019 Juan Manuel Mera
# Distributed under the terms of GNU General Public License v3 (GPLv3)

import unittest
import hd
from binascii import unhexlify as unhex

bip39_vectors = [
    {
        'passphrase': b'HODL',
        'mnemonic': b'gap own cram expect trim name middle magic grid',
        'seed': '8071689d82bd9ef99c2a36dfb9cdc311bf970d13f0cedd93c81f91eb4cb76cb6b77150d51efc450904514e9b44c0c5817327baff93cc89b71af273617421448b'
    },
    {
        'passphrase': b'HODL',
        'mnemonic': b'yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow yellow',
        'seed': '9349ac424dd8fd32fe7a8d6956aab80eed4f56341e02114b775a471b3cde13c02d66ced75b80ec1613dda4c7f4a2181653ce3fba19a3bf9b268d19b686284abc'
    },
    {
        'passphrase': b'HODL',
        'mnemonic': b'clarify wild clog zone intact bright rich program cereal educate love illegal talk mushroom salt bacon mutual light',
        'seed': 'e5e360a4be4c64524dbf450a986498c47f352533d5e988388c4773d28200bcc98158a5eade27e151db4c735b994c5e2ae3c7b7daac59c1322ec94f4c9e0266be'
    },
    {
        'passphrase': b'HODL',
        'mnemonic': b'butter vocal crew machine fiction put artefact loop used intact gain awful trend abstract track room potato govern endless wedding swim moon cabbage vault',
        'seed': 'eeb775918e98d95cfb3c5c12a2ac71d7cdc368e600280abb5165b2274d13b05dc028a5ae51126492f8793a94e8c0327080cc001e7ef1185d5f50a56b5bbc59a3'
    },
    {
        'passphrase': b'BuY',
        'mnemonic': b'slogan tomato this drill virus skirt element relax plastic there uncover soap',
        'seed': '863ce212056c3b86dab64b099b1c060a942cd4b3a66b00b3291e5cb06ca0b2a5386df70d9e4f80a0127e7af38fc93ad86a26219bd14539a520ff22e4f65e9cc6'
    },
    {
        'passphrase': b'',
        'mnemonic': b'damage news brush popular morning bottom accuse sun clump cake chat chapter',
        'seed': '4e63d29cc09a870e2dd07364e9e4fef1e960cdef314e1e5658a010c75374af2ebb0c9d5cb80e2cd1602c49453da24dd09cb0e2f0c01140fa27de6d1e78aa9b08'
    }
]

bip32_vectors = [
    {
        'seed': '000102030405060708090a0b0c0d0e0f',
        'chain': [
            {
                'path': 'm',
                'xpub': b'xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8',
                'xprv': b'xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi'
            },
            {
                'path': 'm/0H',
                'xpub': b'xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvgGDnw',
                'xprv': b'xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7'
            },
            {
                'path': 'm/0H/1',
                'xpub': b'xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ',
                'xprv': b'xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs'
            },
            {
                'path': 'm/0H/1/2H',
                'xpub': b'xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7DogT5Uv6fcLW5',
                'xprv': b'xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4mLTj34bhnZX7UiM'
            },
            {
                'path': 'm/0H/1/2H/2',
                'xpub': b'xpub6FHa3pjLCk84BayeJxFW2SP4XRrFd1JYnxeLeU8EqN3vDfZmbqBqaGJAyiLjTAwm6ZLRQUMv1ZACTj37sR62cfN7fe5JnJ7dh8zL4fiyLHV',
                'xprv': b'xprvA2JDeKCSNNZky6uBCviVfJSKyQ1mDYahRjijr5idH2WwLsEd4Hsb2Tyh8RfQMuPh7f7RtyzTtdrbdqqsunu5Mm3wDvUAKRHSC34sJ7in334'
            },
            {
                'path': 'm/0H/1/2H/2/1000000000',
                'xpub': b'xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy',
                'xprv': b'xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76'
            }
        ]
    },
    {
        'seed': 'fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542',
        'chain': [
            {
                'path': 'm',
                'xpub': b'xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB',
                'xprv': b'xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U'
            },
            {
                'path': 'm/0',
                'xpub': b'xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH',
                'xprv': b'xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt'
            },
            {
                'path': 'm/0/2147483647H',
                'xpub': b'xpub6ASAVgeehLbnwdqV6UKMHVzgqAG8Gr6riv3Fxxpj8ksbH9ebxaEyBLZ85ySDhKiLDBrQSARLq1uNRts8RuJiHjaDMBU4Zn9h8LZNnBC5y4a',
                'xprv': b'xprv9wSp6B7kry3Vj9m1zSnLvN3xH8RdsPP1Mh7fAaR7aRLcQMKTR2vidYEeEg2mUCTAwCd6vnxVrcjfy2kRgVsFawNzmjuHc2YmYRmagcEPdU9'
            },
            {
                'path': 'm/0/2147483647H/1',
                'xpub': b'xpub6DF8uhdarytz3FWdA8TvFSvvAh8dP3283MY7p2V4SeE2wyWmG5mg5EwVvmdMVCQcoNJxGoWaU9DCWh89LojfZ537wTfunKau47EL2dhHKon',
                'xprv': b'xprv9zFnWC6h2cLgpmSA46vutJzBcfJ8yaJGg8cX1e5StJh45BBciYTRXSd25UEPVuesF9yog62tGAQtHjXajPPdbRCHuWS6T8XA2ECKADdw4Ef'
            },
            {
                'path': 'm/0/2147483647H/1/2147483646H',
                'xpub': b'xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGRjaDMzQLcgJvLJuZZvRcEL',
                'xprv': b'xprvA1RpRA33e1JQ7ifknakTFpgNXPmW2YvmhqLQYMmrj4xJXXWYpDPS3xz7iAxn8L39njGVyuoseXzU6rcxFLJ8HFsTjSyQbLYnMpCqE2VbFWc'
            },
            {
                'path': 'm/0/2147483647H/1/2147483646H/2',
                'xpub': b'xpub6FnCn6nSzZAw5Tw7cgR9bi15UV96gLZhjDstkXXxvCLsUXBGXPdSnLFbdpq8p9HmGsApME5hQTZ3emM2rnY5agb9rXpVGyy3bdW6EEgAtqt',
                'xprv': b'xprvA2nrNbFZABcdryreWet9Ea4LvTJcGsqrMzxHx98MMrotbir7yrKCEXw7nadnHM8Dq38EGfSh6dqA9QWTyefMLEcBYJUuekgW4BYPJcr9E7j'
            }
        ]
    },
    {
        'seed': '4b381541583be4423346c643850da4b320e46a87ae3d2a4e6da11eba819cd4acba45d239319ac14f863b8d5ab5a0d0c64d2e8a1e7d1457df2e5a3c51c73235be',
        'chain': [
            {
                'path': 'm',
                'xpub': b'xpub661MyMwAqRbcEZVB4dScxMAdx6d4nFc9nvyvH3v4gJL378CSRZiYmhRoP7mBy6gSPSCYk6SzXPTf3ND1cZAceL7SfJ1Z3GC8vBgp2epUt13',
                'xprv': b'xprv9s21ZrQH143K25QhxbucbDDuQ4naNntJRi4KUfWT7xo4EKsHt2QJDu7KXp1A3u7Bi1j8ph3EGsZ9Xvz9dGuVrtHHs7pXeTzjuxBrCmmhgC6',
            },
            {
                'path': 'm/0H',
                'xpub': b'xpub68NZiKmJWnxxS6aaHmn81bvJeTESw724CRDs6HbuccFQN9Ku14VQrADWgqbhhTHBaohPX4CjNLf9fq9MYo6oDaPPLPxSb7gwQN3ih19Zm4Y',
                'xprv': b'xprv9uPDJpEQgRQfDcW7BkF7eTya6RPxXeJCqCJGHuCJ4GiRVLzkTXBAJMu2qaMWPrS7AANYqdq6vcBcBUdJCVVFceUvJFjaPdGZ2y9WACViL4L',
            }
        ]
    }
]


class TestHD(unittest.TestCase):
    def test_bip32_derivation(self):
        for v, vector in enumerate(bip32_vectors):
            mk = hd.bip32.PrivateKey.from_seed(unhex(vector['seed']))
            for chain in vector['chain']:
                child = mk.child_path(chain['path'])
                self.assertEqual(child.serialize(), chain['xprv'], '{} / {} / xprv'.format(v+1, chain['path']))
                self.assertEqual(child.public().serialize(), chain['xpub'], '{} / {} / xpub'.format(v+1, chain['path']))

    def test_bip32_address(self):
        mnemonic = b'habit frame broom oxygen drastic liberty amused cup image dad obvious someone secret light velvet'
        seed = hd.bip39.to_seed(mnemonic, b'HODL')
        mk = hd.bip32.PrivateKey.from_seed(seed)
        child = mk.child_path('m/44H/0H/0H/0')
        private_key_0 = child.child(0)
        public_key_0 = private_key_0.public()
        self.assertEqual(private_key_0.encode(), b'KxSN8f1in6HVFnjza7jYm1fKXngAhQZqsjMoGvXMJ9yk9z6MWoQC')
        self.assertEqual(public_key_0.encode(), b'12PzQcLP5kKZbLvZbJStm6NV4LiwRLnoG5')
        private_key_42 = child.child(42)
        public_key_42 = private_key_42.public()
        self.assertEqual(private_key_42.encode(), b'L1djiZwSTn4HB84XoQKfXc4Qrz5TT7a4kCDRoNZU2q64ETmganpN')
        self.assertEqual(public_key_42.encode(), b'1Q9uPRydpMGKyGKtrZ4qWsFejfXNnWBG2g')

    def test_bip39_to_seed(self):
        for vector in bip39_vectors:
            seed = hd.bip39.to_seed(vector['mnemonic'], vector['passphrase'])
            self.assertEqual(seed.hex(), vector['seed'], 'Seed: {}'.format(vector['mnemonic']))

    def test_base58_raw_encode(self):
        encoded = hd.base58.raw_encode(b'\x60\x61\x90\x91')
        self.assertEqual(encoded, b'3TtamW')

    def test_base58_raw_decoded(self):
        decoded = hd.base58.raw_decode(b'3TtamW')
        self.assertEqual(decoded, b'\x60\x61\x90\x91')


if __name__ == '__main__':
    unittest.main()