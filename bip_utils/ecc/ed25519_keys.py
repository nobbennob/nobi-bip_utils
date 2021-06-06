# Copyright (c) 2021 Emanuele Bellocchia
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


# Imports
from __future__ import annotations
from nacl import exceptions, signing
from typing import Any, Union
from bip_utils.ecc.elliptic_curve_types import EllipticCurveTypes
from bip_utils.ecc.ikeys import IPoint, IPublicKey, IPrivateKey
from bip_utils.ecc.key_bytes import KeyBytes


class Ed25519Point(IPoint):
    """ Ed25519 point class. """

    def __init__(self,
                 x: int,
                 y: int) -> None:
        """ Construct class from point coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        self.m_x = x
        self.m_y = y

    @staticmethod
    def CurveType() -> EllipticCurveTypes:
        """ Get the elliptic curve type.

        Returns:
           EllipticCurveTypes: Elliptic curve type
        """
        return EllipticCurveTypes.ED25519

    def UnderlyingObject(self) -> Any:
        """ Get the underlying object.

        Returns:
           Any: Underlying object
        """
        return None

    def X(self) -> int:
        """ Get point X coordinate.

        Returns:
           int: Point X coordinate
        """
        return self.m_x

    def Y(self) -> int:
        """ Get point Y coordinate.

        Returns:
           int: Point Y coordinate
        """
        return self.m_y

    def __add__(self,
                point: IPoint) -> IPoint:
        """ Add point to another point.

        Args:
            point (IPoint object): IPoint object

        Returns:
            IPoint object: IPoint object
        """

        # Not needed
        pass

    def __radd__(self,
                 point: IPoint) -> IPoint:
        """ Add point to another point.

        Args:
            point (IPoint object): IPoint object

        Returns:
            IPoint object: IPoint object
        """

        # Not needed
        pass

    def __mul__(self,
                scalar: int) -> IPoint:
        """ Multiply point by a scalar.

        Args:
            scalar (int): scalar

        Returns:
            IPoint object: IPoint object
        """

        # Not needed
        pass

    def __rmul__(self,
                 scalar: int) -> IPoint:
        """ Multiply point by a scalar.

        Args:
            scalar (int): scalar

        Returns:
            IPoint object: IPoint object
        """

        # Not needed
        pass


class Ed25519PublicKey(IPublicKey):
    """ Ed25519 public key class. """

    def __init__(self,
                 key_data: Union[bytes, IPoint]) -> None:
        """ Construct class from key bytes or point and curve.

        Args:
            key_data (bytes or IPoint object): key bytes or point

        Raises:
            ValueError: If key data is not valid
        """
        if isinstance(key_data, bytes):
            self.m_ver_key = self.__FromBytes(key_data)
        # Creation from point not supported
        else:
            raise TypeError("Invalid public key data type")

    @staticmethod
    def CurveType() -> EllipticCurveTypes:
        """ Get the elliptic curve type.

        Returns:
           EllipticCurveTypes: Elliptic curve type
        """
        return EllipticCurveTypes.ED25519

    @staticmethod
    def IsValid(key_data: Union[bytes, IPoint]) -> bool:
        """ Return if the specified data represents a valid public key.

        Args:
            key_data (bytes or IPoint object): key bytes or point

        Returns:
            bool: True if valid, false otherwise
        """
        try:
            Ed25519PublicKey(key_data)
            return True
        except ValueError:
            return False

    def UnderlyingObject(self) -> Any:
        """ Get the underlying object.

        Returns:
           Any: Underlying object
        """
        return self.m_ver_key

    def RawCompressed(self) -> KeyBytes:
        """ Return raw compressed public key.

        Returns:
            KeyBytes object: KeyBytes object
        """
        return KeyBytes(b"\x00" + bytes(self.m_ver_key))

    def RawUncompressed(self) -> KeyBytes:
        """ Return raw uncompressed public key.

        Returns:
            KeyBytes object: KeyBytes object
        """

        # Same as compressed
        return self.RawCompressed()

    def Point(self) -> IPoint:
        """ Get public key point.

        Returns:
            IPoint object: IPoint object
        """

        # Not needed
        pass

    @staticmethod
    def __FromBytes(key_bytes: bytes) -> signing.VerifyingKey:
        """ Get public key from bytes.

        Args:
            key_bytes (bytes): key bytes

        Returns:
            signing.VerifyingKey: signing.VerifyingKey object
        """

        # Remove the first 0x00 if present
        if len(key_bytes) == 33 and key_bytes[0] == 0:
            key_bytes = key_bytes[1:]

        try:
            return signing.VerifyKey(key_bytes)
        except (exceptions.RuntimeError, exceptions.ValueError) as ex:
            raise ValueError("Invalid public key bytes") from ex


class Ed25519PrivateKey(IPrivateKey):
    """ Ed25519 private key class. """

    def __init__(self,
                 key_bytes: bytes) -> None:
        """ Construct class from key bytes and curve.

        Args:
            key_bytes (bytes): key bytes

        Raises:
            ValueError: If key bytes are not valid
        """
        try:
            self.m_sign_key = signing.SigningKey(key_bytes)
        except (exceptions.RuntimeError, exceptions.ValueError) as ex:
            raise ValueError("Invalid private key bytes") from ex

    @staticmethod
    def CurveType() -> EllipticCurveTypes:
        """ Get the elliptic curve type.

        Returns:
           EllipticCurveTypes: Elliptic curve type
        """
        return EllipticCurveTypes.ED25519

    @staticmethod
    def IsValid(key_bytes: bytes) -> bool:
        """ Return if the specified bytes represent a valid private key.

        Args:
            key_bytes (bytes): key bytes

        Returns:
            bool: True if valid, false otherwise
        """
        try:
            Ed25519PrivateKey(key_bytes)
            return True
        except ValueError:
            return False

    def UnderlyingObject(self) -> Any:
        """ Get the underlying object.

        Returns:
           Any: Underlying object
        """
        return self.m_sign_key

    def Raw(self) -> KeyBytes:
        """ Return raw private key.

        Returns:
            KeyBytes object: KeyBytes object
        """
        return KeyBytes(bytes(self.m_sign_key))

    def PublicKey(self) -> Ed25519PublicKey:
        """ Get the public key correspondent to the private one.

        Returns:
            Ed25519PublicKey object: Ed25519PublicKey object
        """
        return Ed25519PublicKey(bytes(self.m_sign_key.verify_key))
