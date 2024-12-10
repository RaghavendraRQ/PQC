from Crypto.Hash import SHAKE256

from core.utils.advbits import bit_unpack
from core.utils.bits import int_to_bytes


class Sample:

    def __init__(self, const):
        self.const = const
        self.shake_256 = None

    def sample_in_ball(self, seed):
        """
        Samples a polynomial in the R with coeff {-1, 0, 1} and hamming weight <= 64

        Args:
            seed: seed for the random number generator

        Returns:
            List[int]: A Polynomial in R
        """

        polynomial = [0] * 256
        shake_256 = SHAKE256.new()
        shake_256.update(seed)
        pass

    def rej_ntt_polynomial(self, seed):
        pass

    def rej_bounded_polynomial(self, seed):
        pass

    def expand_A(self, seed):
        """
        Samples a Matrix A from T^k*l
        Args:
            seed: a 32 byte string for RBG

        Returns:
            Matrix of List: A_cap from Tq
        """
        A = [[[0] * 256 for _ in range(self.const.L)] for _ in range(self.const.K)]
        print(f'A: {len(A)} X {len(A[0])} X {len(A[0][0])}')
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
            self.shake_256 = SHAKE256.new(seed_)
            v = self.shake_256.read(32 * c)
            y[i] = bit_unpack(v, self.const.GAMMA_1 - 1, self.const.GAMMA_1)
        return y
