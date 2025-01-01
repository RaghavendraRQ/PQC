from typing import Tuple, List, Any
from core.utils.overflow.stubborn import NTTModified, VectorNTT

class Encodings:
    const: Any
    public_key_length: int
    private_key_length: int
    signature_length: int

    def __init__(self, const) -> None: ...

    def public_key_encode(self, seed: bytes, t1: VectorNTT) -> bytes: ...

    def public_key_decode(self, public_key: bytes) -> Tuple[bytes, VectorNTT]: ...

    def private_key_encode(self, seed: bytes, k: bytes, tr: bytes, s1: VectorNTT, s2: VectorNTT, t0: VectorNTT) -> bytes: ...

    def private_key_decode(self, private_key: bytes) -> Tuple[bytes, bytes, bytes, VectorNTT, VectorNTT, VectorNTT]: ...
    
    def sign_encode(self, c_hat: bytes, signer_response: VectorNTT, hint: VectorNTT) -> bytes: ...

    def sign_decode(self, sigma: bytes) -> Tuple[bytes, VectorNTT, VectorNTT]: ...

    def w1_encode(self, commitment: VectorNTT) -> bytes: ...
