import core.constants.dsa44 as const
from core.subroutines.MLDSA_ import MLDSA_
from core.utils.dsa.sampling import Sample
from Crypto.Random import get_random_bytes

mldsa = MLDSA_(const)
sample = Sample(const)

seed = get_random_bytes(32)
pk, sk = mldsa.keygen(seed)
message = [1, 0, 0]
signature = mldsa.sign(sk, message, get_random_bytes(32))


print(f'pk: {pk}')
print(f'sk: {sk}')
print(f'signature: {signature}')
print(f'verified: {mldsa.verify(pk, message, signature)}')
