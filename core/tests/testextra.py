import core.constants.dsa44 as const
from core.utils.overflow.stubborn import NTTModified, VectorNTT
from core.utils.dsa.sampling import Sample
from Crypto.Random import get_random_bytes

en = Sample(const)
seed = get_random_bytes(const.LAMBDA // 4)
print(en.sample_in_ball(seed))
