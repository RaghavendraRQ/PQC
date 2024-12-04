from core.utils.ntt import NTT
from core.constants import ETA


ntt = NTT()
seed = b"This is a 32-byte seed used for NT"
ntt_coefficients = ntt.get_sample_ntt(seed)
seed = b"This is a 64-byte seed used for CBD but it is not a multiple s23" * ETA
polynomial = ntt.get_sample_polyCBD(seed)
print(f'sample ntt: {ntt_coefficients}')
print(f'sample tq: {polynomial}')
polynomial = list(range(256))

f_cap = ntt.ntt(ntt_coefficients)
f = ntt.ntt_inverse(f_cap)
print(f'f: {f}')
print(f'f_cap: {f_cap}')
print(f'f equals to ntt coefficients: {f == ntt_coefficients}')

