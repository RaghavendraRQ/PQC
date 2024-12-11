import core.constants.dsa44 as config
from Crypto.Random import get_random_bytes

from core.utils.dsa.sampling import Sample


sam = Sample(config)

ply = sam.rej_ntt_polynomial(get_random_bytes(34))
print(ply)
vec = sam.expand_mask(get_random_bytes(64), 3)
print(vec)
A = sam.expand_A(get_random_bytes(32))
print(A)
