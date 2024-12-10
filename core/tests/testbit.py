import core.constants.dsa44 as const
from core.utils.dsa.sampling import Sample

sample = Sample(const)
seed = bytes(32)
print(sample.expand_mask(seed, 2))
