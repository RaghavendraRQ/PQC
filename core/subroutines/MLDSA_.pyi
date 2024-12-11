from typing import Tuple, Any, List

from core.utils.dsa.sampling import Sample

class MLDSA_:
    const: Any
    sample: Sample
    def __init__(self, const: Any) -> None: ...

    def keygen(self, seed: bytes) -> Tuple[bytes, bytes]: ...

    def sign(self, private_key: bytes, message: List[int], randomness: bytes) -> bytes: ...

    def verify(self, public_key: bytes, message: List[int], signature: bytes) -> bool: ...
