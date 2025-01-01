from typing import Tuple, Any, List, Optional

from core.utils.dsa.encodings import Encodings
from core.utils.dsa.sampling import Sample
from core.utils.overflow.stubborn import VectorNTT

class MLDSA_:
    const: Any
    sample: Sample
    encoding: Encodings
    check: Optional[VectorNTT]

    def __init__(self, const: Any) -> None: ...

    def keygen(self, seed: bytes) -> Tuple[bytes, bytes]: ...

    def sign(self, private_key: bytes, message: List[int], randomness: bytes) -> bytes: ...

    def verify(self, public_key: bytes, message: List[int], signature: bytes) -> bool: ...

    def _encode_message(self, tr: bytes, message: bytes, length: int): ...

    def count_ones(self, hint: VectorNTT) -> int: ...
