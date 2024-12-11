from core.utils.dsa.sampling import Sample
import core.constants.dsa44 as const
from Crypto.Random import get_random_bytes

sample = Sample(const)
b = get_random_bytes(32)
print(sample.sample_in_ball(b))
b = get_random_bytes(34)
print(sample.rej_ntt_polynomial(b))
b = get_random_bytes(66)
print(sample.rej_bounded_polynomial(b))
b = get_random_bytes(32)
print(sample.expand_A(b))
b = get_random_bytes(64)
print(len(sample.expand_S(b)))
