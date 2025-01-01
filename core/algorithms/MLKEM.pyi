from typing import Tuple, Optional, Any
from core.subroutines.MLKEM_ import MLKEM_


class MLKEM:
    MLKEM512: str
    MLKEM768: str
    MLKEM1024: str

    config: Any
    _MLKEM_: MLKEM_
    encapsulation_key: bytes
    decapsulation_key: bytes
    cipher: bytes
    shared_secret: bytes

    def __init__(self, params_set: Optional[str] = MLKEM512) -> None: ...

    def key_gen(self) -> Tuple[bytes, bytes]: ...

    def encapsulation(self, encapsulation_key: bytes) -> Tuple[bytes, bytes]: ...

    def decapsulation(self, decapsulation_key: bytes, cipher: bytes) -> bytes: ...