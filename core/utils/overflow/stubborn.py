from enum import Enum
from typing import List


class ConstantMeta(type):
    def __setattr__(cls, key, value):
        if key in cls.__dict__:
            raise AttributeError(f"{key} is Constant, cannot be modified.")
        super().__setattr__(key, value)


class Ring(Enum):
    RQ = 1
    TQ = 0


class NTTModified:

    def __init__(self, config, polynomial=None, ring=Ring.RQ):
        self.polynomial = polynomial or ([0] * 256)
        self.config = config
        self.Ring = ring

    @property
    def ring(self):
        return self.Ring

    def ntt(self):
        if self.ring == Ring.TQ:
            return self
        polynomial = self.polynomial.copy()
        m = 0
        length = 128
        while length >= 1:
            start = 0
            while start < 256:
                m += 1
                z = self.config.ZETA_VALUES[m]
                for j in range(start, start + length):
                    t = (z * polynomial[j + length]) % self.config.Q
                    polynomial[j + length] = (polynomial[j] - t) % self.config.Q
                    polynomial[j] = (polynomial[j] + t) % self.config.Q
                start += 2 * length
            length //= 2
        return NTTModified(self.config, polynomial, Ring.TQ)

    def inverse(self):
        if self.ring == Ring.RQ:
            return self
        polynomial = self.polynomial.copy()
        m = 256
        length = 1
        while length < 256:
            start = 0
            while start < 256:
                m -= 1
                z = -self.config.ZETA_VALUES[m]
                for j in range(start, start + length):
                    t = polynomial[j]
                    polynomial[j] = (t + polynomial[j + length]) % self.config.Q
                    polynomial[j + length] = (z * (t - polynomial[j + length])) % self.config.Q
                start += 2 * length
            length *= 2

        for i in range(256):
            polynomial[i] = (polynomial[i] * self.config.NTT_SCALE_FACTOR) % self.config.Q

        return NTTModified(self.config, polynomial, Ring.RQ)

    def __add__(self, other):
        result = [(self_x + other_x) % self.config.Q for self_x, other_x in zip(self.polynomial, other.polynomial)]
        return NTTModified(self.config, result)

    def __mul__(self, other):
        result = [(self_x * other_x) % self.config.Q for self_x, other_x in zip(self.polynomial, other.polynomial)]
        return NTTModified(self.config, result)

    def __repr__(self):
        return f'NTT {self.ring}: len({len(self.polynomial)}), {self.polynomial[0:10]} ...'


class VectorNTT:

    def __init__(self, config, vector=None, ring=Ring.TQ):
        self.config = config
        self.vector = vector or [NTTModified(self.config) for _ in range(self.config.L)]
        self.Ring = ring or vector[0].ring

    def __repr__(self):
        return (f'VectorNTT object: len ({len(self.vector)})'
                f'\n\t{self.vector[0]}, '
                f'\n\t{self.vector[-1]}\n'
                )

    def __add__(self, other):
        return VectorNTT(self.config, [self_ntt + other_ntt for self_ntt, other_ntt in zip(self.vector, other.vector)])

    def __mul__(self, other):
        if isinstance(other, NTTModified):
            return VectorNTT(self.config, [self_ntt + other for self_ntt in self.vector])
        if isinstance(other, List):
            result = VectorNTT(self.config, [NTTModified(self.config) for _ in range(self.config.K)])
            for i in range(self.config.K):
                for j in range(self.config.L):
                    result.vector[j] = result.vector[j] + (self.vector[j] * other[i].vector[j])
            return result

