import core.constants.dsa44 as config
from Crypto.Random import get_random_bytes

from core.subroutines.MLDSA_ import MLDSA_

ml = MLDSA_(config)
pk, sk = ml.keygen(get_random_bytes(32))
message = [1, 0, 0]
sign = ml.sign(sk, message, get_random_bytes(32))


print(f'verified: {ml.verify(pk, message, sign)}')


