from typing import Tuple, Any, Union
from core.subroutines.KPke import KPke


class ML_KEM_Internal:
    const: Any
    kpke: KPke
    encapsulation_key: Union[bytes, None]
    decapsulation_key: Union[bytes, None]

    def __init__(self, const: Any) -> None: ...

    def keygen(self, d: bytes, z: bytes) -> Tuple[bytes, bytes]: ...

    def encapsulation(self, m: bytes, encapsulation_key: bytes) -> Tuple[bytes, bytes]: ...

    def decapsulation(self, c: bytes, decapsulation_key: bytes) -> bytes: ...