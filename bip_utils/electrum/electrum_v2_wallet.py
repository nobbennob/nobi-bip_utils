# Copyright (c) 2022 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Module containing utility classes for Electrum v2 wallet keys derivation, since it uses its own paths."""

# Imports
from abc import ABC, abstractmethod
from functools import lru_cache
from bip_utils.addr import P2PKHAddr, P2WPKHAddr
from bip_utils.bip.bip32 import Bip32PrivateKey, Bip32PublicKey, Bip32Base
from bip_utils.coin_conf import CoinsConf


class ElectrumV2WalletBase(ABC):
    """Electrum v2 wallet base class."""

    m_bip32: Bip32Base

    def __init__(self,
                 bip32: Bip32Base) -> None:
        """
        Construct class.

        Args:
            bip32 (Bip32Base object): Bip32Base object
        """
        self.m_bip32 = bip32

    def Bip32Object(self) -> Bip32Base:
        """
        Return the BIP32 object.

        Returns:
            Bip32Base object: Bip32Base object
        """
        return self.m_bip32

    @abstractmethod
    def GetPrivateKey(self,
                      change_idx: int,
                      addr_idx: int) -> Bip32PrivateKey:
        """
        Get the private key with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            Bip32PrivateKey object: Bip32PrivateKey object
        """

    @abstractmethod
    def GetPublicKey(self,
                     change_idx: int,
                     addr_idx: int) -> Bip32PublicKey:
        """
        Get the public key with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            Bip32PublicKey object: Bip32PublicKey object
        """

    @abstractmethod
    def GetAddress(self,
                   change_idx: int,
                   addr_idx: int) -> str:
        """
        Get the address with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            str: Address
        """


class ElectrumV2WalletStandard(ElectrumV2WalletBase):
    """Electrum v2 standard wallet class."""

    def __init__(self,
                 bip32: Bip32Base) -> None:
        """
        Construct class.

        Args:
            bip32 (Bip32Base object): Bip32Base object
        """
        super().__init__(bip32)

    def GetPrivateKey(self,
                      change_idx: int,
                      addr_idx: int) -> Bip32PrivateKey:
        """
        Get the private key with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            Bip32PrivateKey object: Bip32PrivateKey object
        """
        return self.__DeriveKey(change_idx, addr_idx).PrivateKey()

    def GetPublicKey(self,
                     change_idx: int,
                     addr_idx: int) -> Bip32PublicKey:
        """
        Get the public key with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            Bip32PublicKey object: Bip32PublicKey object
        """
        return self.__DeriveKey(change_idx, addr_idx).PublicKey()

    def GetAddress(self,
                   change_idx: int,
                   addr_idx: int) -> str:
        """
        Get the address with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            str: Address
        """
        return P2PKHAddr.EncodeKey(self.GetPublicKey(change_idx, addr_idx).KeyObject(),
                                   net_ver=CoinsConf.BitcoinMainNet.Params("p2pkh_net_ver"))

    @lru_cache()
    def __DeriveKey(self,
                    change_idx: int,
                    addr_idx: int) -> Bip32Base:
        """
        Derive the key with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            Bip32Base object: Bip32Base object
        """
        return self.m_bip32.DerivePath(f"m/{change_idx}/{addr_idx}")


class ElectrumV2WalletSegwit(ElectrumV2WalletBase):
    """Electrum v2 segwit wallet class."""

    m_bip32_acc: Bip32Base

    def __init__(self,
                 bip32: Bip32Base) -> None:
        """
        Construct class.

        Args:
            bip32 (Bip32Base object): Bip32Base object
        """
        super().__init__(bip32)
        self.m_bip32_acc = bip32.DerivePath("m/0'")

    def GetPrivateKey(self,
                      change_idx: int,
                      addr_idx: int) -> Bip32PrivateKey:
        """
        Get the private key with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            Bip32PrivateKey object: Bip32PrivateKey object
        """
        return self.__DeriveKey(change_idx, addr_idx).PrivateKey()

    def GetPublicKey(self,
                     change_idx: int,
                     addr_idx: int) -> Bip32PublicKey:
        """
        Get the public key with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            Bip32PublicKey object: Bip32PublicKey object
        """
        return self.__DeriveKey(change_idx, addr_idx).PublicKey()

    def GetAddress(self,
                   change_idx: int,
                   addr_idx: int) -> str:
        """
        Get the address with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            str: Address
        """
        return P2WPKHAddr.EncodeKey(self.GetPublicKey(change_idx, addr_idx).KeyObject(),
                                    hrp=CoinsConf.BitcoinMainNet.Params("p2wpkh_hrp"))

    @lru_cache()
    def __DeriveKey(self,
                    change_idx: int,
                    addr_idx: int) -> Bip32Base:
        """
        Derive the key with the specified change and address indexes.

        Args:
            change_idx (int): Change index
            addr_idx (int)  : Address index

        Returns:
            Bip32Base object: Bip32Base object
        """
        return self.m_bip32_acc.DerivePath(f"{change_idx}/{addr_idx}")
