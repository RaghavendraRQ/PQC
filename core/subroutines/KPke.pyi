from typing import Tuple, List, Any, Union
from core.utils.ntt import NTT

Matrix = List[List[int]]

class KPke:
    ntt: NTT
    k: int
    const: Any
    encryption_key: Union[bytes, None]
    decryption_key: Union[bytes, None]

    def __init__(self, const: Any) -> None: ...

    def keygen(self, d: bytes) -> Tuple[bytes, bytes]: ...

    def encrypt(self, message: bytes, randomness: bytes, encryption_key: bytes) -> bytes: ...

    def decrypt(self, cipher: bytes, decryption_key: bytes) -> bytes: ...

    def _multiply_vector_vector(self, vec1: Matrix, vec2: Matrix) -> List[int]: ...

    def _multiply_array_vector_modified(self, array: List[Matrix], vector: Matrix) -> Matrix: ...

    def _multiply_array_transpose_vector(self, array: List[Matrix], vector: Matrix) -> Matrix: ...

    def _add_vectors(self, vec1: Matrix | List[int], vec2: Matrix | List[int]) -> Matrix | List[int]: ...
