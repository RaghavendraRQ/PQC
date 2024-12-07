from typing import Tuple, Optional, Any
from core.subroutines.ML_KEM_Internal import ML_KEM_Internal


class MLKEM:
    MLKEM512: str
    MLKEM768: str
    MLKEM1024: str

    def __init__(self, params_set: Optional[str] = MLKEM512) -> None:
        self.config: Any = None
        self._ml_kem_internal: ML_KEM_Internal = None
        self.encapsulation_key: bytes = None
        self.decapsulation_key: bytes = None
        self.cipher: bytes = None
        self.shared_secret: bytes = None

    def key_gen(self) -> Tuple[bytes, bytes]: ...

    def encapsulation(self, encapsulation_key: bytes) -> Tuple[bytes, bytes]: ...

    def decapsulation(self, decapsulation_key: bytes, cipher: bytes) -> bytes: ...