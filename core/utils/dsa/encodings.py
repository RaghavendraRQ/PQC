from core.utils.advbits import simple_bit_pack, simple_bit_unpack, bit_pack, bit_unpack, hint_bit_pack, hint_bit_unpack
from core.utils.overflow.stubborn import NTTModified, VectorNTT
import logging

logging.basicConfig(level=logging.INFO)


class Encodings:

    def __init__(self, const):
        self.const = const

    def public_key_encode(self, r0, t1):
        """
        Encodes the public key to a byte string

        Args:
            r0: byte string
            t1: NTT object

        Returns:
            bytes: encoded public key
        """

        public_key = r0
        length = self.const.N
        for i in range(self.const.K):
            public_key += simple_bit_pack(t1[i], length)

        return public_key

    def public_key_decode(self, public_key):
        """
        Reverse operation of public_key_encode

        Args:
            public_key: public key in byte string

        Returns:
            Tuple[bytes, List[List[int]]]: r0 and t1
        """

        r0 = public_key[:32]
        z = public_key[32:]
        z = [z[i * 320: (i + 1) * 320] for i in range(self.const.K)]
        print(f'z: {len(z)}')
        t1 = [[0] * 256 for _ in range(self.const.K)]
        for i in range(self.const.K):
            t1[i] = simple_bit_unpack(z[i], self.const.N)
        return r0, t1

    def private_key_encode(self, r0, k, tr, s1, s2, t0):
        """
        Encodes a secret key for ML-DSA into a byte string.
        Args:
            r0: 32 byte string
            k: 32 byte string
            tr: 64 byte string
            s1: Matrix of integers (L)
            s2: Matrix of integers (K)
            t0: Matrix of integers (K)

        Returns:
            A private key in byte string
        """
        assert len(r0) == len(k) == len(tr) // 2 == 32, (f"Length of r0, k, tr should be 32 bytes {len(r0), len(k)}"
                                                         f"{len(tr)}")
        assert s1.check(-self.const.ETA, self.const.ETA), "All Coefficients should be in range [-ETA, ETA]"
        assert s2.check(-self.const.ETA, self.const.ETA), "All Coefficients should be in range [-ETA, ETA]"
        assert t0.check(-2 ** (self.const.D - 1) + 1, 2 ** (self.const.D - 1)), (
            "All Coefficients should be in range"
            "[2 ^(D -1) + 1, 2^(D-1)]")

        private_key = r0 + k + tr
        for i in range(self.const.L):
            private_key += bit_pack(s1[i].polynomial, self.const.ETA, self.const.ETA)
        for i in range(self.const.K):
            private_key += bit_pack(s2[i].polynomial, self.const.ETA, self.const.ETA)
        for i in range(self.const.K):
            private_key += bit_pack(t0[i].polynomial, 2 ** (self.const.D - 1) - 1, 2 ** (self.const.D - 1))
        return private_key

    def private_key_decode(self, private_key):
        """
        Reverse operation of private_key_encode

        Args:
            private_key: private key in byte string

        Returns:
            Tuple: r0, k, tr, s1, s2, t0
        """
        r0 = private_key[:32]
        k = private_key[32: 64]
        tr = private_key[64: 128]
        y = private_key[128: 512]
        n = len(y) // self.const.L
        y = [y[i * n: (i + 1) * n] for i in range(self.const.L)]
        z = private_key[512:896]
        n = len(z) // self.const.K
        z = [z[i * n: (i + 1) * n] for i in range(self.const.K)]
        w = private_key[896:]
        n = len(w) // self.const.K
        w = [w[i * n: (i + 1) * n] for i in range(self.const.K)]

        s1 = [[0] * 256 for _ in range(self.const.L)]
        s2 = [[0] * 256 for _ in range(self.const.K)]
        t0 = [[0] * 256 for _ in range(self.const.K)]

        for i in range(self.const.L):
            s1[i] = bit_unpack(y[i], self.const.ETA, self.const.ETA)
        for i in range(self.const.K):
            s2[i] = bit_unpack(z[i], self.const.ETA, self.const.ETA)
        for i in range(self.const.K):
            t0[i] = bit_unpack(w[i], 2 ** (self.const.D - 1) - 1, 2 ** (self.const.D - 1))
        return (r0, k, tr,
                VectorNTT(self.const, [NTTModified(self.const, s11) for s11 in s1]),
                VectorNTT(self.const, [NTTModified(self.const, s11) for s11 in s2]),
                VectorNTT(self.const, [NTTModified(self.const, s11) for s11 in t0]),
                )

    def sign_encode(self, c_hat, z, h):
        """
        Encodes a signature into a byte string.
        Args:
            c_hat: Byte String of length Lambda / 4
            z: Matrix of integers (L)
            h: Matrix of integers (K)

        Returns:
            A signature sigma in byte string
        """
        assert len(c_hat) == self.const.LAMBDA // 4, (f"Length of c_hat should be {self.const.LAMBDA // 4} bytes. Not "
                                                      f"{len(c_hat)}")
        assert z.check(-self.const.GAMMA_1 + 1, self.const.GAMMA_1), ("All Coefficients should be in range ["
                                                                      "-GAMMA_1+1, GAMMA_1]")
        assert h.check(0, 1), "All Coefficients should be 0 or 1"

        sigma = c_hat
        for i in range(self.const.L):
            sigma += bit_pack(z[i].polynomial, self.const.GAMMA_1 - 1, self.const.GAMMA_1)
        sigma += hint_bit_pack(h.to_list(), self.const.K, self.const.OMEGA)
        return sigma

    def sign_decode(self, sigma):
        """
        Reverses the operation of sign_encode
        Args:
            sigma: Signature in byte string

        Returns:
            Tuple: c_hat, z, h
        """

        c_hat = sigma[:self.const.LAMBDA // 4]
        x = sigma[self.const.LAMBDA // 4: self.const.LAMBDA // 4 + 32 * self.const.L * (1 + (self.const.GAMMA_1 - 1)
                                                                                        .bit_length())]
        n = len(x) // self.const.L
        x = [x[i * n: (i + 1) * n] for i in range(self.const.L)]
        y = sigma[-(self.const.OMEGA + self.const.K):]
        z = [[0] * 256 for _ in range(self.const.L)]
        for i in range(self.const.L):
            z[i] = bit_unpack(x[i], self.const.GAMMA_1 - 1, self.const.GAMMA_1)

        h = hint_bit_unpack(y, self.const.K, self.const.OMEGA)
        return c_hat, z, h

    def w1_encode(self, w1):
        """
        Encodes a polynomial vector w1 into a byte string

        Args:
            w1: Matrix of integers (K)

        Returns:
            A byte string of w1
        """
        # assert w1.check(0, (self.const.Q - 1) // (2 * self.const.GAMMA_2) - 1), "Coefficients are too high"

        w1_ = b''
        for i in range(self.const.K):
            w1_ += simple_bit_pack(w1[i].polynomial, (self.const.Q - 1) // (2 * self.const.GAMMA_2) - 1)
        return w1_
