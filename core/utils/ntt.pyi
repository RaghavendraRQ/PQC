from typing import List, Tuple, Any

class NTT:
    zeta_values: Tuple[int]
    zeta_double_value: Tuple[int]
    n: int
    q: int
    eta: int

    def __init__(self, const: Any) -> None: ...

    def ntt(self, f: List[int]) -> List[int]: ...

    def ntt_inverse(self, f_cap: List[int]) -> List[int]: ...

    def multiply_ntt(self, f_cap: List[int], g_cap: List[int]) -> List[int]: ...

    def get_sample_ntt(self, byte_array: bytes) -> List[int]: ...

    def get_sample_polyCBD(self, byte_array: bytes, eta: int) -> List[int]: ...

    def _base_case_multiply(self, a0:int, a1:int, b0:int, b1:int, zeta:int) -> Tuple[int, int]: ...




