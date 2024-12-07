import numpy as np

from core.utils.bits import byte_encode, byte_decode, compress, decompress
from core.utils.hash import sha3_512, prf
from core.utils.ntt import NTT


class KPke:
    def __init__(self, const):
        """
        Initializes a KPke object with a random seed

        :param const: constants used for different algorithms
        """
        self.ntt = NTT(const)
        self.const = const
        self.k = const.K
        self.encryption_key = None
        self.decryption_key = None

    def keygen(self, d):
        """
        Generates a pair of keys for encryption and decryption. which have length based on the implementation

        :param d: a random 32 bytes for randomness

        :return: Tuple of (encryption_key, decryption_key)
        """
        if self.encryption_key is not None and self.decryption_key is not None:
            return self.encryption_key, self.decryption_key

        assert len(d) == 32, f"Length of random bytes {32}bytes. Not {len(d)}"

        ro, sigma = sha3_512(d + self.k.to_bytes())
        n = 0
        s = [[0] * self.const.N for _ in range(self.k)]
        e = [[0] * self.const.N for _ in range(self.k)]
        A = [[[0] * self.const.N for _ in range(self.k)] for _ in range(self.k)]
        for i in range(self.k):
            for j in range(self.k):
                A[i][j] = self.ntt.get_sample_ntt(ro + j.to_bytes() + i.to_bytes())
        for i in range(self.k):
            s[i] = self.ntt.get_sample_polyCBD(prf(sigma, n.to_bytes(), self.const.ETA), self.const.ETA)
            n += 1
        for j in range(self.k):
            e[j] = self.ntt.get_sample_polyCBD(prf(sigma, n.to_bytes(), self.const.ETA), self.const.ETA)
            n += 1
        s_cap = [self.ntt.ntt(s[i]) for i in range(self.k)]
        e_cap = [self.ntt.ntt(e[i]) for i in range(self.k)]
        t_cap = self._add_vectors(self._multiply_array_vector_modified(A, s_cap), e_cap)
        self.encryption_key = b''.join([byte_encode(t_cap[i], 12) for i in range(self.k)]) + ro
        self.decryption_key = b''.join([byte_encode(s_cap[i], 12) for i in range(self.k)])
        return self.encryption_key, self.decryption_key

    def encrypt(self, message, randomness, encryption_key):
        """
        Generates a cipher text for the given message using encryption_key

        :param message: (Byte) 32 byte message
        :param randomness: (Byte) 32 byte random value
        :param encryption_key: (Byte) encryption_key of size 384k + 32

        :return: (Byte) return a cipher text of length 384k + 32
        """

        assert len(message) == 32 and len(randomness) == 32, f"Length of message and randomness should be {32} bytes."

        self.encryption_key = encryption_key
        A = [[[0] * self.const.N for _ in range(self.k)] for _ in range(self.k)]
        n = 0
        t_cap = [byte_decode(self.encryption_key[i * 384: (i + 1) * 384], self.const.D) for i in range(self.k)]
        ro = self.encryption_key[384 * self.k: 384 * self.k + 32]
        for i in range(self.k):
            for j in range(self.k):
                A[i][j] = self.ntt.get_sample_ntt(ro + j.to_bytes() + i.to_bytes())
        y = [[0] * self.const.N for _ in range(self.k)]
        e1 = [[0] * self.const.N for _ in range(self.k)]
        for i in range(self.k):
            y[i] = self.ntt.get_sample_polyCBD(prf(randomness, n.to_bytes(), self.const.ETA), self.const.ETA)
            n += 1
        for j in range(self.k):
            e1[j] = self.ntt.get_sample_polyCBD(prf(randomness, n.to_bytes(), self.const.ETA_2), self.const.ETA_2)
            n += 1
        e2 = self.ntt.get_sample_polyCBD(prf(randomness, n.to_bytes(), self.const.ETA_2), self.const.ETA_2)
        y_cap = [self.ntt.ntt(y[i]) for i in range(self.k)]
        u = self._multiply_array_transpose_vector(A, y_cap)
        u = [self.ntt.ntt_inverse(u[i]) for i in range(self.k)]
        u = [self._add_vectors(u[i], e1[i]) for i in range(self.k)]
        mu = decompress(byte_decode(message, 1), 1)
        v = self.ntt.ntt_inverse(self._multiply_vector_vector(t_cap, y_cap))
        v = self._add_vectors(self._add_vectors(v, e2), mu)
        first_half_cipher = [byte_encode(compress(u[i], self.const.DU), self.const.DU) for i in range(self.k)]
        second_half_cipher = byte_encode(compress(v, self.const.DV), self.const.DV)
        cipher = b''.join(first_half_cipher)
        cipher += second_half_cipher
        return cipher

    def decrypt(self, cipher, decryption_key):
        """
        Decrypts a cipher text to get original message back

        :param cipher: a cipher text of length 384k + 32
        :param decryption_key: a decryption_key corresponding to cipher text

        :return: a message of length 32 bytes
        """
        self.decryption_key = decryption_key
        first_half = cipher[0:32 * self.const.DU * self.k]
        second_half = cipher[32 * self.const.DU * self.k:]
        u = [decompress(byte_decode(first_half[32 * self.const.DU * i: 32 * self.const.DU * (i + 1)], self.const.DU),
                        self.const.DU) for i in range(self.k)]
        v = decompress(byte_decode(second_half, self.const.DV), self.const.DV)
        s_cap = [byte_decode(self.decryption_key[i * 384: (i + 1) * 384], 12) for i in range(self.k)]
        u_cap = [self.ntt.ntt(u[i]) for i in range(self.k)]
        w = self.ntt.ntt_inverse(self._multiply_vector_vector(s_cap, u_cap))
        w = np.subtract(v, w) % self.const.Q
        message = byte_encode(compress(w, 1), 1)
        return message

    def _multiply_vector_vector(self, vec1, vec2):
        result = [0] * self.const.N
        for i in range(self.k):
            result = self._add_vectors(self.ntt.multiply_ntt(vec1[i], vec2[i]), result)
        return result

    def _multiply_array_vector_modified(self, array, vector):
        result = [[0] * self.const.N for _ in range(self.k)]
        for i in range(self.k):
            for j in range(self.k):
                result[i] = self._add_vectors(self.ntt.multiply_ntt(array[i][j], vector[j]), result[i])
        return result

    def _multiply_array_transpose_vector(self, array, vector):
        result = [[0] * self.const.N for _ in range(self.k)]
        for i in range(self.k):
            for j in range(self.k):
                result[i] = self._add_vectors(self.ntt.multiply_ntt(array[j][i], vector[j]), result[i])
        return result

    def _add_vectors(self, vec1, vec2):
        return np.add(vec1, vec2) % self.const.Q
