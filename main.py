from core.utils.sampleNtt import sample_ntt, sample_poly_cbd
from core.utils.ntt import ntt, ntt_inverse, multiply_ntt

seed = b"This is a 32-byte seed used for NT"
ntt_coefficients = sample_ntt(seed)
eta = 2
seed = b"This is a 64-byte seed used for CBD but it is not a multiple s23" * eta
# polynomial = sample_poly_cbd(seed, eta)
polynomial = list(range(256))
f_cap = ntt(polynomial)
print(f'f_cap: {f_cap}')
f = ntt_inverse(f_cap)
print(f'f: {f}')
print(f'f == polynomial: {f == polynomial}')
g_cap = ntt(polynomial)
h_cap = multiply_ntt(f_cap, g_cap)
print(f'h_cap: {h_cap}')
