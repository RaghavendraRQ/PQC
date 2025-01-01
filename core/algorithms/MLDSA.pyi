from typing import Tuple, List, Any, Optional, Union
from core.subroutines.MLDSA_ import MLDSA_


class MLDSA:
    MLDSA44: str
    MLDSA65: str
    MLDSA87: str
    config: Any
    _mldsa: MLDSA_

    def __init__(self, params_set: Optional[Union[MLDSA44, MLDSA87, MLDSA65]]=MLDSA44) -> None: ...

    def keygen(self) -> Tuple[bytes, bytes]: ...

    def sign(self, private_key: bytes, message: List[int], ctx: bytes) -> bytes: ...

    def verify(self, public_key: bytes, message: List[int], signature: bytes, ctx: bytes) -> bool: ...

