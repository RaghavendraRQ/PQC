import core.constants.dsa44 as config
from Crypto.Random import get_random_bytes

from core.utils.dsa.sampling import Sample
from core.subroutines.MLDSA_ import MLDSA_


sam = Sample(config)
ml = MLDSA_(config)
pk, sk = ml.keygen(get_random_bytes(32))
sign = ml.sign(sk, [0, 1, 1], get_random_bytes(32))
print(f'pk: {pk}')
print(f'sk: {sk}')
print(f'sign: {sign}')
