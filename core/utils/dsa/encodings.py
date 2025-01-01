from core.utils.advbits import simple_bit_pack, simple_bit_unpack, bit_pack, bit_unpack, hint_bit_pack, hint_bit_unpack
from core.utils.overflow.stubborn import VectorNTT
import logging

logging.basicConfig(level=logging.INFO)


class Encodings:

    def __init__(self, const):
        self.const = const
        # 32 + 32k(q.butt_size - d)
        self.public_key_length = 32 + 32 * self.const.K * (self.const.Q.bit_length() - self.const.D)
        # 32 + 32 + 64 + 32(kl * 2eta.butt_size + dk)
        self.private_key_length = 128 + 32 * ((self.const.K + self.const.L) * (2 * self.const.ETA).bit_length()
                                              + self.const.D * self.const.K)
        # lambda / 4 + 32l(gamma_1.butt_size + 1) + k+omega
        self.signature_length = (self.const.LAMBDA // 4 + 32 * self.const.L * (1 + (self.const.GAMMA_1 - 1)
                                                                               .bit_length()) +
                                 self.const.K + self.const.OMEGA)

    def public_key_encode(self, seed, t1):
        """
        Encodes the public key to a byte string

        Args:
            seed: byte string
            t1: NTT object

        Returns:
            bytes: encoded public key
        """
        if not len(seed) == 32:
            raise ValueError("Length of seed should be 32 bytes")

        public_key = seed
        length = self.const.N
        for i in range(self.const.K):
            public_key += simple_bit_pack(t1[i], length)

        assert len(public_key) == self.public_key_length, f"Length of public key should be {self.public_key_length}"
        return public_key

    def public_key_decode(self, public_key):
        """
        Reverse operation of public_key_encode

        Args:
            public_key: public key in byte string

        Returns:
            Tuple: seed and t1
        """
        if not len(public_key) == self.public_key_length:
            raise ValueError(f"Length of public key should be {self.public_key_length}")

        seed = public_key[:32]
        signer_response = public_key[32:]
        part_length = len(signer_response) // self.const.K
        signer_response = [signer_response[i * part_length: (i + 1) * part_length] for i in
                           range(self.const.K)]  # This is danger...
        t1 = VectorNTT(self.const)

        for i in range(self.const.K):
            t1[i] = simple_bit_unpack(signer_response[i], self.const.N)
        return seed, t1

    def private_key_encode(self, seed, k, tr, s1, s2, t0):
        """
        Encodes a secret key for ML-DSA into a byte string.

        Args:
            seed: 32 byte string
            k: 32 byte string
            tr: 64 byte string
            s1: VectorNTT (L)
            s2: VectorNTT (K)
            t0: VectorNTT (K)

        Returns:
            A private key in byte string format
        """
        if not len(seed) == len(k) == len(tr) // 2 == 32:
            raise ValueError("Length of seed, k, tr should be 32 bytes {len(seed), len(k), len(tr)}")
        assert s1.check(-self.const.ETA, self.const.ETA), "All Coefficients should be in range [-ETA, ETA]"
        assert s2.check(-self.const.ETA, self.const.ETA), "All Coefficients should be in range [-ETA, ETA]"
        assert t0.check(-2 ** (self.const.D - 1) + 1, 2 ** (self.const.D - 1)), (
            "All Coefficients should be in range"
            "[2 ^(D -1) + 1, 2^(D-1)]")

        private_key = seed + k + tr
        for i in range(self.const.L):
            private_key += bit_pack(s1[i], self.const.ETA, self.const.ETA)
        for i in range(self.const.K):
            private_key += bit_pack(s2[i], self.const.ETA, self.const.ETA)
        for i in range(self.const.K):
            private_key += bit_pack(t0[i], 2 ** (self.const.D - 1) - 1, 2 ** (self.const.D - 1))

        assert len(private_key) == self.private_key_length, f"We Fucked Up privately!! It is {self.private_key_length}"
        return private_key

    def private_key_decode(self, private_key):
        """
        Reverse operation of private_key_encode

        Args:
            private_key: private key in byte string

        Returns:
            Tuple: seed(bytes), k(bytes), tr(bytes), s1(VectorNTT), s2(VectorNTT), t0(VectorNTT)
        """
        if not len(private_key) == self.private_key_length:
            raise ValueError(f"Length of private key should be {self.private_key_length}")

        # Unpacking the shit
        seed = private_key[:32]
        k = private_key[32: 64]
        tr = private_key[64: 128]
        y = private_key[128: 512]
        n = len(y) // self.const.L
        y = [y[i * n: (i + 1) * n] for i in range(self.const.L)]
        signer_response = private_key[512:896]
        n = len(signer_response) // self.const.K
        signer_response = [signer_response[i * n: (i + 1) * n] for i in range(self.const.K)]
        w = private_key[896:]
        n = len(w) // self.const.K
        w = [w[i * n: (i + 1) * n] for i in range(self.const.K)]

        # initialize the vectors
        s1 = VectorNTT(self.const)
        s2 = VectorNTT(self.const)
        t0 = VectorNTT(self.const)

        for i in range(self.const.L):
            s1[i] = bit_unpack(y[i], self.const.ETA, self.const.ETA)
        for i in range(self.const.K):
            s2[i] = bit_unpack(signer_response[i], self.const.ETA, self.const.ETA)
        for i in range(self.const.K):
            t0[i] = bit_unpack(w[i], 2 ** (self.const.D - 1) - 1, 2 ** (self.const.D - 1))
        return seed, k, tr, s1, s2, t0  # I know there is a lot to unpack. But trust me, It works.

    def sign_encode(self, c_hat, signer_response, hint):
        """
        Encodes a signature into a byte string.

        Args:
            c_hat: Byte String of length Lambda / 4
            signer_response: Matrix of integers (L)
            hint: Matrix of integers (K)

        Returns:
            A signature sigma in byte string
        """
        if not len(c_hat) == self.const.LAMBDA // 4:
            raise ValueError(f"Length of c_hat should be {self.const.LAMBDA // 4} bytes. Not {len(c_hat)}")
        if not signer_response.check(-self.const.GAMMA_1 + 1, self.const.GAMMA_1):
            raise ValueError("All Coefficients should be in range [-GAMMA_1+1, GAMMA_1]")
        if not hint.check(0, 1):
            raise ValueError("All Coefficients should be 0 or 1")

        sigma = c_hat
        for i in range(self.const.L):
            sigma += bit_pack(signer_response[i], self.const.GAMMA_1 - 1, self.const.GAMMA_1)
        sigma += hint_bit_pack(hint, self.const.K, self.const.OMEGA)

        assert len(sigma) == self.signature_length, f"We Fucked Up in signing!! It is not {self.signature_length}"
        return sigma

    def sign_decode(self, sigma):
        """
        Reverses the operation of sign_encode
        Args:
            sigma: Signature in byte string

        Returns:
            Tuple: c_hat, signer_response, hint
        """
        if not len(sigma) == self.signature_length:
            raise ValueError(f"Hey Don't test my patience. Length of sigma should be {self.signature_length}")

        c_hat = sigma[:self.const.LAMBDA // 4]
        x = sigma[self.const.LAMBDA // 4: self.const.LAMBDA // 4 + 32 * self.const.L * (1 + (self.const.GAMMA_1 - 1)
                                                                                        .bit_length())]
        n = len(x) // self.const.L
        packed_response = [x[i * n: (i + 1) * n] for i in range(self.const.L)]
        packed_hint = sigma[-(self.const.OMEGA + self.const.K):]

        signer_response = VectorNTT(self.const)
        for i in range(self.const.L):
            # This is in the correct range as per the check in sign_encode
            signer_response[i] = bit_unpack(packed_response[i], self.const.GAMMA_1 - 1, self.const.GAMMA_1)
        hint = hint_bit_unpack(packed_hint, self.const.K, self.const.OMEGA)
        return c_hat, signer_response, hint     # Happy? Less to unpack now.

    def w1_encode(self, commitment):
        """
        Encodes a polynomial vector commitment into a byte string

        Args:
            commitment: VectorNTT object (K)

        Returns:
            A byte string of w1
        """
        upper_limit = (self.const.Q - 1) // (2 * self.const.GAMMA_2) - 1
        if not commitment.check(0, upper_limit):
            raise ValueError("All Coefficients should be in range [0, (Q-1) / (2 * GAMMA_2) - 1]")

        commitment_encoded = b''
        # This is a bit tricky. We are encoding the commitment in a bit packed format.
        for i in range(self.const.K):
            commitment_encoded += simple_bit_pack(commitment[i], upper_limit)

        assert len(commitment_encoded) == 32 * self.const.K * upper_limit.bit_length()
        return commitment_encoded # size: 32 * K * bitlen((Q.bit_size - 1) // (2 * GAMMA_2) - 1)

