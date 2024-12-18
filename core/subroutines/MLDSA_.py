from Crypto.Hash import SHAKE256

from core.utils.bits import int_to_bytes, bytes_to_bits
from core.utils.dsa.sampling import Sample
from core.utils.dsa.encodings import Encodings
from core.utils.overflow.stubborn import VectorNTT
from core.utils.optimizers import power2_round, high_bits, low_bits, make_hint, mod_symmetric, use_hint


class MLDSA_:

    def __init__(self, const):
        self.const = const
        self.sample = Sample(const)
        self.encoding = Encodings(self.const)
        self.check = None

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
        print(f't (keygen): {t}')
        self.check = t
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
        counter, iterations = 0, 0
        c_hat = None
        signer_response, hint = None, None
        while signer_response is None or hint is None:
            iterations += 1
            y = self.sample.expand_mask(seed_mask, counter)
            w = (y.ntt() * matrix_vector).inverse()
            commitment = w.apply(high_bits, self.const.Q, self.const.GAMMA_2)
            c_hat = SHAKE256.new(repr_message + self.encoding.w1_encode(commitment)).read(self.const.LAMBDA // 4)
            challenge = self.sample.sample_in_ball(c_hat)
            c_cap = challenge.ntt()
            rs1 = (s1_cap * c_cap).inverse()
            rs2 = (s2_cap * c_cap).inverse()
            signer_response = y + rs1
            r0 = (w - rs2).apply(low_bits, self.const.Q, self.const.GAMMA_2)
            if signer_response.norm() >= (self.const.GAMMA_1 - self.const.BETA) or r0.norm() >= (self.const.GAMMA_2 -
                                                                                                 self.const.BETA):
                print(f'Trying ...')
                signer_response, hint = None, None
            else:
                rs0 = (t0_cap * c_cap).inverse()
                hint = (-rs0).apply(make_hint, self.const.Q, self.const.GAMMA_2, other=(w - rs2) + rs0)
                if rs0.norm() >= self.const.GAMMA_2 or self.count_ones(hint) > self.const.OMEGA:
                    print(f'Edge case detected.Trying ...')
                    signer_response, hint = None, None
            counter += self.const.L
        print(f'successful after {iterations} iterations')
        print('***********Prover side************')
        print(f'commitment: {commitment}')
        print('*********************************')
        signature = self.encoding.sign_encode(c_hat, signer_response.apply(mod_symmetric, self.const.Q), hint)
        return signature

    def verify(self, public_key, message, signature):
        """
        Verifies the signature of a message
        Args:
            public_key: byte string representation of public key
            message: bit string of a message
            signature: byte string of a signature

        Returns:
            bool: True if signature is valid, False otherwise
        """
        seed_A, t1 = self.encoding.public_key_decode(public_key)
        c_hat, signer_response, hint = self.encoding.sign_decode(signature)
        if hint is None:
            print('Argh! Here we go again')
            return False
        matrix_vector = self.sample.expand_A(seed_A)
        tr = SHAKE256.new(public_key).read(64)
        repr_message = self._encode_message(tr, bytes(message), 64)
        challenge = self.sample.sample_in_ball(c_hat)

        scaled_t1 = (t1 * (2 ** self.const.D))
        scaled_t1 = scaled_t1.apply(lambda x: x % self.const.Q).ntt()
        scaled_t1 = self.check.ntt()
        commitment_approx = (
                (signer_response.ntt() * matrix_vector) - (scaled_t1 * challenge.ntt())
        ).inverse()
        commitment = hint.apply(use_hint, self.const.Q, self.const.GAMMA_2, other=commitment_approx)

        c_hat_decoded = SHAKE256.new(repr_message + self.encoding.w1_encode(commitment)).read(self.const.LAMBDA // 4)
        print('***********Verifier side************')
        print(f'scaled_t1: {scaled_t1}')
        print('************************************')
        return c_hat == c_hat_decoded and signer_response.norm() < (self.const.GAMMA_1 - self.const.BETA)

    @staticmethod
    def _encode_message(tr, message, length):
        return SHAKE256.new(bytes(bytes_to_bits(tr)) + message).read(length)

    def count_ones(self, hint):
        count = 0
        for i in range(self.const.K):
            count += hint[i].polynomial.count(1)
        return count
