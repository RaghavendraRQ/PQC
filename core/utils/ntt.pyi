from typing import List, Tuple
import core.constants_ as cons

class NTT:
    def __init__(self, const: cons) -> None:
        self.zeta_values: Tuple[int] = None
        self.zeta_double_value: Tuple[int] = None
        self.n: int = None
        self.q: int = None
        self.eta: int = None

    def ntt(self, f: List[int]) -> List[int]: ...

    def ntt_inverse(self, f_cap: List[int]) -> List[int]: ...

    def multiply_ntt(self, f_cap: List[int], g_cap: List[int]) -> List[int]: ...

    def get_sample_ntt(self, byte_array: bytes) -> List[int]: ...

    def get_sample_polyCBD(self, byte_array: bytes, eta: int) -> List[int]: ...

    def _base_case_multiply(self, a0:int, a1:int, b0:int, b1:int, zeta:int) -> Tuple[int, int]: ...




