from core.utils.bits import bytes_to_bits
from Crypto.Hash import SHAKE128


class NTT:
    """
    Creates a NTT class
    Attributes:
        zeta_values: All the zeta values that are corresponding to the algorithm
        zeta_double_value: All the zeta square values  that are corresponding to the algorithm
        n: size of the NTT functions in Rq
        q: Modulus
        eta: Constant value
    """
    def __init__(self, const):
        self.zeta_values = const.ZETA_VALUES
        self.zeta_double_value = const.ZETA_DOUBLE_VALUES
        self.n = const.N
        self.q = const.Q
        self.eta = const.ETA

    def ntt(self, f):
        """
        Computes the NTT of a given polynomial f.

        Args:
            f:  Array of polynomial coefficients in Z_q (length 256).

        Returns:
            Array of NTT coefficients f_cap in Z_q.
        """
        assert len(f) == 256, f"Length of array f should be {256}, Not {len(f)}"

        f_cap = f.copy()
        i = 1
        length = 128
        while length >= 2:
            for start in range(0, 256, 2 * length):
                zeta = self.zeta_values[i]
                i += 1
                for j in range(start, start + length):
                    t = (zeta * f_cap[j + length]) % self.q
                    f_cap[j + length] = (f_cap[j] - t) % self.q
                    f_cap[j] = (f_cap[j] + t) % self.q
            length //= 2
        return f_cap

    def ntt_inverse(self, f_cap):
        """
        Computes the inverse NTT (NTT_Inverse) of a given NTT representation f_cap.

        Args:
            f_cap: Array of NTT coefficients in Z_q (length 256).

        Returns:
            Array of polynomial coefficients f in Z_q.
        """
        assert len(f_cap) == 256, f"Length of f_cap must be 256. Not {len(f_cap)}."

        f = f_cap.copy()
        i = 127
        length = 2
        while length <= 128:
            for start in range(0, 256, 2 * length):
                zeta = self.zeta_values[i]
                i -= 1
                for j in range(start, start + length):
                    t = f[j]  # Save the value of f[j]
                    f[j] = (t + f[j + length]) % self.q  # f[j] = f[j] + f[j + length]
                    f[j + length] = (zeta * (f[j + length] - t)) % self.q  # f[j+length] = zeta * (f[j+length] - t)
            length *= 2
        scale_factor = 3303
        f = [(x * scale_factor) % self.q for x in f]
        return f

    def _base_case_multiply(self, a0, a1, b0, b1, zeta):
        """
        Computes the coefficient multiplication of two polynomials from T_q

        Args:
            a0: coefficient of x^0 in f_cap
            a1: coefficient of x^1 in f_cap
            b0: coefficient of x^0 in g_cap
            b1: coefficient of x^1 in g_cap
            zeta: corresponding zeta value

        Returns:
            Tuple: c0, c1
        """
        assert 0 <= any([a0, a1, b0, b1]) <= self.q, "All the coefficients should be in range[0, Q]"

        c0 = (a0 * b0 + a1 * b1 * zeta) % self.q
        c1 = (a0 * b1 + a1 * b0) % self.q
        return c0, c1

    def multiply_ntt(self, f_cap, g_cap):
        """
        Computes the multiplication for two elements from T_q

        Args:
            f_cap:  An element from T_q, coefficients for 128 mono-degree polynomial
            g_cap: Another element from T_q, coefficients for 128 mono-degree polynomial

        Returns:
             Multiplication of these two elements
        """
        assert len(f_cap) == 256 and len(g_cap) == 256, (f" Length of f_cap and g_cap must be 256. Not {len(f_cap)} and"
                                                         f" {len(g_cap)}.")

        h_cap = [0] * 256
        for i in range(128):
            h_cap[2 * i], h_cap[2 * i + 1] = self._base_case_multiply(f_cap[2 * i], f_cap[2 * i + 1],
                                                                      g_cap[2 * i], g_cap[2 * i + 1],
                                                                      self.zeta_double_value[i])
        return h_cap

    def get_sample_ntt(self, byte_array):
        """
        Samples a pseudorandom element of T_q using a 34-byte seed and two indices.

        Args:
            byte_array: 34-byte seed (input as a byte array).

        Returns:
            Array of coefficients a ∈ ℤ_256 (NTT coefficients).
        """
        assert len(byte_array) == 34, f"The byte array must be 34 bytes in length. Not {len(byte_array)}."

        shake = SHAKE128.new()
        shake.update(byte_array)
        a = [0] * 256
        j = 0
        while j < 256:
            c = shake.read(3)
            d1 = c[0] + 256 * (c[1] % 16)
            d2 = (c[1] // 16) + 16 * c[2]
            if d1 < self.q:
                a[j] = d1
                j += 1
            if d2 < self.q and j < 256:
                a[j] = d2
                j += 1
        return a

    def get_sample_polyCBD(self, byte_array, eta):
        """
        Samples a pseudorandom polynomial from the distribution D_eta(R_q).

        Args:
            byte_array: Byte array of size 64 * eta (input as a byte array).
            eta: A constant that determines the distribution.

        Returns:
            Array of polynomial coefficients f ∈ ℤ_256.
        """
        eta = eta or self.eta
        expected_length = 64 * eta
        assert len(byte_array) == expected_length, f"The byte array must be of length {expected_length}."
        f"Not {len(byte_array)}"

        bit_array = bytes_to_bits(byte_array)
        f = [0] * 256
        for i in range(256):
            x = sum(bit_array[2 * i * eta + j] for j in range(eta))
            y = sum(bit_array[2 * i * eta + eta + j] for j in range(eta))
            f[i] = (x - y) % self.q
        return f
