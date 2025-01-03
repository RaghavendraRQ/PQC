from typing import List, Optional
from core.utils.overflow.stubborn import NTTModified, VectorNTT

Matrix = VectorNTT

def simple_bit_pack(polynomial: NTTModified, end: int) -> bytes: ...

def simple_bit_unpack(byte_string: bytes, end: int) -> NTTModified: ...

def bit_pack(polynomial: NTTModified, start: int, end: int) -> bytes: ...

def bit_unpack(byte_string: bytes, start: int, end: int) -> NTTModified: ...

def hint_bit_pack(polynomial_vector: Matrix, K: int, OMEGA: int) -> bytes: ...

def hint_bit_unpack(byte_string: bytes, K: int, OMEGA: int) -> Matrix | None: ...
