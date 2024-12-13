from Crypto.Hash import SHAKE256
from Crypto.Random import get_random_bytes

from core.utils.bits import int_to_bytes, bytes_to_bits
from core.utils.dsa.sampling import Sample
from core.utils.dsa.encodings import Encodings
from core.utils.overflow.stubborn import VectorNTT
from core.utils.optimizers import power2_round, high_bits, low_bits, make_hint


class MLDSA_:

    def __init__(self, const):
        self.const = const
        self.sample = Sample(const)
        self.encoding = Encodings(self.const)

    def keygen(self, seed):
        """
        Generates a public private key pair from seed
        Args:
            seed: A Random 32 byte seed

        Returns:
            Tuple: Public key, Private key
        """
        assert len(seed) == 32, "length of the seed should be 32 bytes."

        hashed = SHAKE256.new(seed + int_to_bytes(self.const.K, 1) + int_to_bytes(self.const.L, 1)).read(128)
        seed_A, seed_S, k = hashed[:32], hashed[32:96], hashed[96:]
        matrix_vector = self.sample.expand_A(seed_A)
        s1, s2 = self.sample.expand_S(seed_S)
        t = (s1.ntt() * matrix_vector).inverse() + s2
        t1, t0 = VectorNTT(self.const), VectorNTT(self.const)
        for i in range(self.const.K):
            for j in range(256):
                t1[i][j], t0[i][j] = power2_round(t[i][j], self.const.Q, self.const.D)
        public_key = self.encoding.public_key_encode(seed_A, t1)
        tr = SHAKE256.new(public_key).read(64)
        private_key = self.encoding.private_key_encode(seed_A, k, tr, s1, s2, t0)
        return public_key, private_key

    def sign(self, private_key, message, random):
        """
        Deterministic algorithm to generate a signature for a formatted message M
        Args:
            private_key: byte string representation of private key
            message: bit string of a message
            random: 32 bytes per message randomness or dummy variable

        Returns:
            bytes: Signature of the message
        """
        assert len(random) == 32, "Length of the random number should be 32 bytes"

        seed_A, k, tr, s1, s2, t0 = self.encoding.private_key_decode(private_key)
        s1_cap, s2_cap, t0_cap = s1.ntt(), s2.ntt(), t0.ntt()
        matrix_vector = self.sample.expand_A(seed_A)
        repr_message = self._encode_message(tr, bytes(message), 64)
        seed_mask = SHAKE256.new(k + random + repr_message).read(64)
        counter = 0
        z, h = None, None
        while z == h is None:
            y = self.sample.expand_mask(seed_mask, counter)
            w = (y.ntt() * matrix_vector).inverse()
            w1 = w.apply(high_bits, 0, Q=self.const.Q, GAMMA_2=self.const.GAMMA_2)
            c_hat = SHAKE256.new(repr_message + self.encoding.w1_encode(w1)).read(self.const.LAMBDA // 4)
            c = self.sample.sample_in_ball(c_hat)
            c_cap = c.ntt()
            rs1 = (s1_cap * c_cap).inverse()
            rs2 = (s2_cap * c_cap).inverse()
            print(f'y: {y.norm()}')
            z = y + rs1
            r0 = (w - rs2).apply(low_bits, 0, Q=self.const.Q, GAMMA_2=self.const.GAMMA_2)
            print(f'z: {z.norm()} r0: {r0.norm()}')
            if z.norm() >= (self.const.GAMMA_1 - self.const.BETA) or r0.norm() >= (self.const.GAMMA_2 - self.const.BETA):
                print(f'checking...')
                z, h = None, None
            else:
                rs0 = (t0_cap * c_cap).inverse()
                h = self.compute_make_hint(-rs0, w - rs2 + rs0)
                if rs0.norm() >= self.const.GAMMA_2 or h.norm() > self.const.OMEGA:
                    z, h = None, None
            counter += self.const.L
        print(f'c_hat: {c_hat}')
        signature = self.encoding.sign_encode(c_hat, z, h)
        return signature

    def _encode_message(self, tr, message, length):
        return SHAKE256.new(bytes(bytes_to_bits(tr)) + message).read(length)

    def compute_make_hint(self, vec1, vec2):
        result = VectorNTT(self.const)
        for i in range(self.const.L):
            for j in range(256):
                result[i][j] = make_hint(vec1[i][j], vec2[i][j], self.const.Q, self.const.GAMMA_2)
        return result
