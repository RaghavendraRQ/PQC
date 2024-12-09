from core.utils.optimizers import power2_round, decompose, mod_symmetric, make_hint, use_hint, high_bits, low_bits
import core.constants.dsa44 as const

r = 123456789
z = 987654321

print(mod_symmetric(r, 2 ** const.D))
print(power2_round(r, const.Q, const.D))
print(decompose(r, const.Q, const.GAMMA_2))
print(high_bits(r, const.Q, const.GAMMA_2))
print(low_bits(r, const.Q, const.GAMMA_2))
print(make_hint(z, r, const.Q, const.GAMMA_2))
print(use_hint(True, r, const.Q, const.GAMMA_2))
