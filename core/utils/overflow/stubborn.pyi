from enum import Enum
from typing import List, Optional, Union, Any

class Ring(Enum):
    RQ: int
    TQ: int

class NTTModified:
    config: Any
    polynomial: List[int]
    Ring: Ring

    def __init__(self, config: Any, polynomial: Optional[List[int]] = None, ring: Optional[Ring] = Ring.RQ) -> None: ...

    @property
    def ring(self) -> Ring: ...

    def ntt(self) -> NTTModified: ...

    def inverse(self) -> NTTModified: ...

    def __add__(self, other: NTTModified) -> NTTModified: ...

    def __repr__(self) -> str: ...

    def __mul__(self, other: NTTModified) -> NTTModified: ...

Matrix = List[NTTModified]

class VectorNTT:
    config: Any
    vector: Matrix
    Ring: Ring

    def __init__(self, config, vector: Optional[Matrix]=None, ring: Optional[Ring]=Ring.RQ) -> None: ...

    def __repr__(self) -> str: ...

    def __add__(self, other: VectorNTT) -> VectorNTT: ...

    def __mul__(self, other: Union[NTTModified, List[VectorNTT]]) -> VectorNTT: ...