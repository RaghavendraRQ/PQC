from typing import List, Tuple

Matrix = List[List[int]]

class Sample:

    def __init__(self, const) -> None:
        self.const = None
        self.shake_256 = None

    def sample_in_ball(self, seed: bytes) -> List[int]: ...

    def rej_ntt_polynomial(self, seed: bytes) -> List[int]: ...

    def rej_bounded_polynomial(self, seed: bytes) -> List[int]: ...

    def expand_A(self, seed: bytes) -> List[Matrix]: ...

    def expand_S(self, seed: bytes) -> Tuple[List[int], List[int]]: ...

    def expand_mask(self, seed: bytes, coefficient: int) -> List[int]: ...

