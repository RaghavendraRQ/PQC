from typing import Tuple, Any
from core.subroutines.KPke import KPke


class ML_KEM_Internal:

    def __init__(self, const: Any) -> None:
        self.const: Any = const
        self.kpke: KPke = None
        self.encapsulation_key: bytes = None
        self.decapsulation_key: bytes = None

    def keygen(self, d: bytes, z: bytes) -> Tuple[bytes, bytes]: ...

    def encapsulation(self, m: bytes, encapsulation_key: bytes) -> Tuple[bytes, bytes]: ...

    def decapsulation(self, c: bytes, decapsulation_key: bytes) -> bytes: ...