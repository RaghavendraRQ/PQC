from Crypto.Hash import SHAKE256, SHAKE128

from core.utils.advbits import bit_unpack
from core.utils.bits import int_to_bytes, bytes_to_bits, coeff_from_three_bytes, coeff_from_half_byte


class Sample:

    def __init__(self, const):
        self.const = const

    def sample_in_ball(self, seed):
        """
        Samples a polynomial in the R with coefficients {-1, 0, 1} and hamming weight <= 64

        Args:
            seed: seed for the random number generator

        Returns:
            List[int]: A Polynomial in R
        """

        polynomial = [0] * 256
        shake_256 = SHAKE256.new()
        shake_256.update(seed)
        s = shake_256.read(8)
        h = bytes_to_bits(s)
        for i in range(256 - self.const.TO, 256):
            j = int.from_bytes(shake_256.read(1))
            while j > i:
                j = int.from_bytes(shake_256.read(1))
            polynomial[i] = polynomial[j]
            polynomial[j] = (-1) ** h[i + self.const.TO - 256]

        return polynomial

    def rej_ntt_polynomial(self, seed):
        """
        Samples a polynomial from Tq
        Args:
            seed: A Random byte seed

        Returns:
            List: An element belongs to Tq
        """
        assert len(seed) == 34, "Length of the random seed should be 34 bytes"

        j = 0
        shake_128 = SHAKE128.new()
        shake_128.update(seed)
        a_cap = [0] * 256
        while j < 256:
            s = shake_128.read(3)
            a_cap[j] = coeff_from_three_bytes(s[0].to_bytes(), s[1].to_bytes(), s[2].to_bytes())
            if a_cap[j] is not None:
                j += 1
        return a_cap

    def rej_bounded_polynomial(self, seed):
        """
        Sample an element from R with coefficients [-ETA, ETA] computed via rejection from RO
        Args:
            seed: A Random byte seed

        Returns:
            List: An element belongs to R
        """
        assert len(seed) == 66, "Length of the seed should be 66."

        j = 0
        shake_256 = SHAKE256.new()
        shake_256.update(seed)
        a = [0] * 256
        while j < 256:
            z = int.from_bytes(shake_256.read(1))
            z0 = coeff_from_half_byte(z % 16, self.const.ETA)
            z1 = coeff_from_half_byte(z // 16, self.const.ETA)
            if z0 is not None:
                a[j] = z0
                j += 1
            if z1 is not None and j < 256:
                a[j] = z1
                j += 1
        return a

    def expand_A(self, seed):
        """
        Samples a Matrix A from T^k*l
        Args:
            seed: a 32 byte string for RBG

        Returns:
            Matrix of List: A_cap from Tq
        """
        A = [[[0] * 256 for _ in range(self.const.L)] for _ in range(self.const.K)]
        for i in range(self.const.K):
            for j in range(self.const.L):
                seed_ = seed + int_to_bytes(j, 1) + int_to_bytes(i, 1)
                A[i][j] = self.rej_ntt_polynomial(seed_)

        return A

    def expand_S(self, seed):
        """
        Samples vectors from s1, s2 from Rk with coefficients in range[-ETA, ETA]
        Args:
            seed: 64 byte random string

        Returns:
            Tuple of Matrices: vectors s1, s2
        """

        s1, s2 = [[0] * 256 for _ in range(self.const.L)], [[0] * 256 for _ in range(self.const.K)]
        for i in range(self.const.L):
            s1[i] = self.rej_bounded_polynomial(seed + int_to_bytes(i, 2))
        for i in range(self.const.K):
            s2[i] = self.rej_bounded_polynomial(seed + int_to_bytes(i + self.const.L, 2))

        return s1, s2

    def expand_mask(self, seed, coefficient):
        """
        Samples a vector from Rl coefficients in range[-GAMMA_1 + 1, GAMMA_1]
        Args:
            seed:
            coefficient:

        Returns:

        """
        y = [[0] * 256 for _ in range(self.const.L)]
        c = 1 + (self.const.GAMMA_1 - 1).bit_length()
        for i in range(self.const.L):
            seed_ = seed + int_to_bytes(i + coefficient, 2)
            shake_256 = SHAKE256.new(seed_)
            v = shake_256.read(32 * c)
            y[i] = bit_unpack(v, self.const.GAMMA_1 - 1, self.const.GAMMA_1)
        return y
