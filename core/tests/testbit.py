import core.constants.dsa44 as const
from core.utils.dsa.encodings import Encodings

encoding = Encodings(const)


w1 = [[2] * 256 for _ in range(const.K)]
w1_ = encoding.w1_encode(w1)
print(f'w1: {w1_}')
