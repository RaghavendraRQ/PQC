from core.utils.optimizers import high_bits, mod_symmetric
import core.constants.dsa44 as config

r = 2448666
r1 = high_bits(r, config.Q, config.GAMMA_2)
print(r1)
print(mod_symmetric(19, 5))
